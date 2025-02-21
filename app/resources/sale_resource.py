from flask_restful import Resource
from app.models.sale_model import SaleModel
from flask import request
from app.schemas.sale_schema import (
    CreateSaleSchema,
    SaleSchema,
    CustomerSchema,
    SaleDetailSchema
)
from app.schemas.product_schema import SaleProductSchema
from app.models.customer_model import CustomerModel
from app.models.sale_detail_model import SaleDetailModel
from app.models.product_model import ProductModel
from db import db
from fpdf import FPDF
import io
from flask import send_file, Response

class SaleResource(Resource):
    def get(self):
        try:
            sales = SaleModel.query.all()

            response_data = []
            for sale in sales:
                sale_dict = SaleSchema(
                    id=sale.id,
                    code=sale.code,
                    total=sale.total,
                    status=sale.status,
                    created_at=str(sale.created_at),
                    updated_at=str(sale.updated_at)
                ).model_dump()

                sale_dict['customer'] = CustomerSchema(
                    id=sale.customer.id,
                    name=sale.customer.name,
                    last_name=sale.customer.last_name,
                    email=sale.customer.email,
                    address=sale.customer.address,
                    document_number=sale.customer.document_number
                ).model_dump()

                sale_dict['details'] = []
                for sale_detail in sale.sale_details:
                    sale_detail_dict = SaleDetailSchema(
                        id=sale_detail.id,
                        quantity=sale_detail.quantity,
                        price=sale_detail.price,
                        subtotal=sale_detail.subtotal
                    ).model_dump()

                    sale_detail_dict['product'] = SaleProductSchema(
                        id=sale_detail.product.id,
                        code=sale_detail.product.code,
                        name=sale_detail.product.name,
                    ).model_dump()

                    sale_dict['details'].append(sale_detail_dict)

                response_data.append(sale_dict)

            return response_data, 200
        except Exception as e:
            return {
                'message': 'Unexpected error',
            }, 500

    def post(self):
        try:
            data = request.get_json()
            validated_data = CreateSaleSchema(**data)

            customer = CustomerModel.query.filter_by(
                document_number=validated_data.customer.document_number
            ).first()

            if not customer:
                customer = CustomerModel(
                    name=validated_data.customer.name,
                    last_name=validated_data.customer.last_name,
                    email=validated_data.customer.email,
                    address=validated_data.customer.address,
                    document_number=validated_data.customer.document_number
                )

                db.session.add(customer)
                db.session.flush()
            else:
                customer.name = validated_data.customer.name
                customer.last_name = validated_data.customer.last_name
                customer.email = validated_data.customer.email
                customer.address = validated_data.customer.address

            sale_details = []
            for detail in validated_data.details:
                product = ProductModel.query.get(detail.product_id)
                if not product:
                    raise Exception('Product not found')
                
                if product.status == False:
                    raise Exception('Product is disabled')
                
                if detail.quantity > product.stock:
                    raise Exception('Product out of stock')
                
                # Validar también precio, subtotal, etc

                product.stock -= detail.quantity

                sale_detail = SaleDetailModel(
                    quantity=detail.quantity,
                    price=detail.price,
                    subtotal=detail.subtotal,
                    product_id=product.id
                )
                sale_details.append(sale_detail)

            last_sale = SaleModel.query.order_by(
                SaleModel.id.desc()
            ).first()

            sale_code = 'B-0001'
            if last_sale:
                last_code = last_sale.code
                last_number = int(last_code.split('-')[1])
                new_number = last_number + 1
                sale_code = f'B-{str(new_number).zfill(4)}'

            sale = SaleModel(
                code=sale_code,
                total=validated_data.total,
                customer_id=customer.id,
                sale_details=sale_details
            )

            db.session.add(sale)
            db.session.commit()
            
            return 'Ok', 200
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Unexpected error',
            }, 500
        
class DownloadInvoiceResource(Resource):
    def get(self, sale_id):
        try:
            sale = SaleModel.query.get(sale_id)

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', size=12)
            pdf.cell(200, 10, txt=f'INVOICE {sale.code}', ln=1, align='C')

            pdf_output = pdf.output(dest='S').encode('latin1')

            return send_file(
                pdf_output,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'factura.pdf'
            )
            # return Response(
            #     pdf_output,
            #     mimetype='application/pdf',
            #     headers={
            #         'Content-Disposition': f'attachment; filename=factura.pdf'
            #     }
            # )
        except Exception as e:
            print(e)
            return {
                'message': 'Unexpected error',
            }, 500