from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import QuerySet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics
from .serializer import *
from .models import *
import datetime, jwt

# Create your views here.

def index(request):
    return HttpResponse("<h1> Hello World </h1>")

# ============================ USER API ======================================
class UserView():

    # Đăng ký thông tin tài khoản
    @api_view(['POST'])
    def register(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    

    # Đăng nhập thông tin tài khoản
    @api_view(['POST'])
    def login(request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")
        
        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)

        cursor = User.objects.raw("SELECT * FROM core_user u WHERE u.username = %s", [request.data["username"]])

        user = UserSerializer(cursor, many=True).data

        # Lấy role của tk
        cursor = Role.objects.raw("SELECT r.* FROM core_user u JOIN core_user_role ur ON u.id = ur.user_id JOIN core_role r ON ur.role_id = r.id WHERE u.username = %s", [request.data["username"]])

        role = RoleSerializer(cursor, many=True).data

        response.data = {
            'jwt': token,
            'user': user,
            'role': role
        }

        return response

    # Đăng xuất thông tin tài khoản
    @api_view(['POST'])
    def logout(self):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "success"
        }
    
    # Tìm kiếm thông tin người dùng
    @api_view(['GET'])
    def search_user(self, request):
        params = request.GET 
        keyword = params.get('keyword', '')
        user_list = User.objects.filter(QuerySet(username__icontains=keyword) | QuerySet(email__icontains=keyword) | QuerySet(phone__icontains=keyword))
        serializer = UserSerializer(user_list, many=True)

        return Response(serializer.data)

    # Liệt kê danh sách người dùng
    @api_view(['GET'])
    def list_user(request):
        user_list = User.objects.all()
        serializer = UserSerializer(user_list, many=True)
        return Response({"Message": "List of User", "User List": serializer.data})
    

    # Liệt kê danh sách quản lý
    @api_view(['GET'])
    def list_user_manage(request):
        list_manage = User.objects.raw("SELECT u.* FROM core_user u JOIN core_user_role ur ON u.id = ur.user_id" +
                                        " JOIN core_role r ON ur.role_id = r.id WHERE r.role_name = 'ADMIN'")
        
        serializer = UserSerializer(list_manage, many=True)
        return Response(serializer.data)
    
    # Liệt kê danh sách khách hàng
    @api_view(['GET'])
    def list_user_customer(request):
        list_customer = User.objects.raw("SELECT u.* FROM core_user u JOIN core_user_role ur ON u.id = ur.user_id" +
                                        " JOIN core_role r ON ur.role_id = r.id WHERE r.role_name = 'CUSTOMER'")

        serializer = UserSerializer(list_customer, many=True)
        return Response(serializer.data)

    # Cập nhật thông tin người dùng
    @api_view(['PUT'])
    def update_user(request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "sucess", "Data": serializer.data})
        else:
            return Response({"Message": "error", "Error": serializer.errors})
    
    # Xóa thông tin người dùng
    @api_view(['DELETE'])
    def delete_user(request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.status = 0

            user.save()
            return Response({"Message": "Success"})
        except Exception as e:
            return Response({"Message": "error", "Error": str(e)})

    
    # Tạo tài khoản mới
    @api_view(['POST'])
    def create_user(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors, status=404)
    
# ===============================================================================



# ======================== SUPPLIER API =========================================
class SupplierView():
    # Tạo mới nhà cung cấp
    @api_view(['POST'])
    def create_supplier(request):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=404)
        
    
    # Lấy danh sách các nhà cung cấp
    @api_view(['GET'])
    def list_supplier(request):
        supplier = Supplier.objects.all()
        serializer = SupplierSerializer(supplier, many=True)
        return Response(serializer.data)
    # Tìm kiếm nhà cung cấp
    @api_view(['GET'])
    def search_supplier(request):
        params = request.GET
        keyword = params.get('keyword', '')
        supplier = Supplier.objects.filter(QuerySet(supplier_name__icontains=keyword) | QuerySet(phone__icontains=keyword))
        serializer = SupplierSerializer(supplier, many=True)
        return Response(serializer.data)

    # Cập nhật thông tin nhà cung cấp
    @api_view(['PUT'])
    def update_supplier(request, pk):
        supplier = Supplier.objects.get(pk=pk)
        serializer = SupplierSerializer(supplier, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "success", "Data": serializer.data})
        else: 
            return Response({"Message": "error", "Error": serializer.errors})
    
    # Xóa thông tin nhà cung cấp
    @api_view(['DELETE'])
    def delete_supplier(request, pk):
        try:
            supplier = Supplier.objects.get(pk=pk)
            supplier.delete()

            return Response({"Message": "sucesss"})
        except Exception as e:
            return Response({"Message": "error", "Error": str(e)})
# ===============================================================================

# ================================ CATEGORY API =================================
class CategoryView():
    # Tạo mới danh mục 
    @api_view(['POST'])
    def create_category(request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=404)
    
    # Hiển thị danh sách các danh mục 
    @api_view(['GET'])
    def list_category(request):
        queryset = Category.objects.all()
        categorys = []

        for category in queryset:
            categorys.append({"id": category.id, "category_name": category.category_name, "create_date": category.create_date,
                            "create_by": category.create_by.username, "update_date": category.update_date, "update_by": category.update_by.username})
        
        return Response(categorys)
    
    # Tìm kiếm danh mục
    @api_view(['GET'])
    def search_category(request):
        params = request.GET
        keyword = params.get('keyword', '')
        category = Category.objects.filter(QuerySet(category_name__icontains=keyword))
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
    
    # Lấy danh sách danh mục theo id
    @api_view(['GET'])
    def get_category_by_id(request, pk):
        list_category = Category.objects.raw("SELECT * FROM core_category WHERE id = %s", [pk])
        serializer = CategorySerializer(list_category, many=True)

        return Response(serializer.data)
    
    # Cập nhật thông tin danh mục 
    @api_view(['PUT'])
    def update_category(request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "success", "Data": serializer.data})
        else:
            return Response({"Message": "error", "Data": serializer.errors})
    
    # Xóa thông tin danh mục
    @api_view(['DELETE'])
    def delete_category(request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response({"Message": "success"})
        except Exception as e:
            return Response({"Message": "error", "Error": str(e)})
# ===============================================================================


# ================================== API BRANCH =================================
class BranchView():
    # Tạo mới thương hiệu
    @api_view(['POST'])
    def create_branch(request):
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else: 
            return Response(serializer.errors, status=404)
    
    # Hiển thị danh sách các nhãn hiệu
    @api_view(['GET'])
    def list_branch(request):
        queryset = Branch.objects.all()
        branchs = []

        for branch in queryset:
            branchs.append({"id": branch.id, 'branch_name': branch.branch_name, 'create_date': branch.create_date,
                            "create_by": branch.create_by.username, 'update_by': branch.update_by.username, 'update_date': branch.update_date})

        return Response(branchs)

    # Cập nhật thông tin nhãn hàng
    @api_view(['PUT'])
    def update_branch(request, pk):
        branch = Branch.objects.get(pk=pk)
        serializer = BranchSerializer(branch, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "Success", "Data": serializer.data})
        else:
            return Response({"Message": "error", "Error": serializer.errors})
    

    # Xóa danh sách các nhãn hàng
    @api_view(['DELETE'])
    def delete_branch(request, pk):
        try:
            branch = Branch.objects.get(pk=pk)
            branch.delete()

            return Response({"Message": "sucess"})
        except Exception as e:
            return Response({"Message": "error", "Error": str(e)})
# ===============================================================================


# ========================= API TICKER IMPORT ===================================
class TicketImportView():
    # Hiển thị danh sách phiếu nhập hàng
    @api_view(['GET'])
    def ticket_list(request):
        queryset = Ticket_import.objects.select_related('supplier')
        tickets = []
        for ticket in queryset:
            tickets.append({"id": ticket.id, "code": ticket.code ,"supplier": ticket.supplier.supplier_name, "total_price": ticket.total_price, "create_date": ticket.create_date, "supplier_id": ticket.supplier.id})
        return Response(tickets)

    # Xóa thông tin đơn nhập hàng
    @api_view(['DELETE'])
    def delete_ticket(request, pk):
        try:
            ticketimport = Ticket_import.objects.get(pk=pk)
            ticketimport.status = 0

            ticketimport.save()
            return Response({"Message": "sucess"})
        except Exception as e:
            return Response({"Message": "error", "Error": str(e)})
        
    @api_view(['POST'])
    def create_ticket_import(request):
        serializer = TicketImportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
        
class TickerAPIView(generics.GenericAPIView):
    serializer_class = TicketImportSerializer

    def post(self, request, *args, **kwargs):
        data = request.data or []

        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        
        return Response(serializer.data)
# ===============================================================================

# ======================= IMPORT DETAIL API =====================================
class ImportDetailView():
    # Tạo mới chi tiết đơn hàng
    @api_view(['POST'])
    def create_ticketdetail(request):
        serializer = TicketDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    

    # Lấy danh sách chi tiết đơn hàng
    @api_view(['GET'])
    def ticketdetail_by_id(request, pk):
        ticketdetail = Ticket_Import_Detail.objects.get(pk=pk)
        serializer = TicketDetailSerializer(ticketdetail, many=True)
        return Response(serializer.data)

    # Cập nhật thông tin chi tiết đơn hàng
    @api_view(['PUT'])
    def update_ticketdetail(request, pk):
        ticketdetail = Ticket_Import_Detail.objects.get(pk=pk)
        serializer = TicketDetailSerializer(ticketdetail, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "success", "Data": serializer.data})
        else:
            return Response({"Message": "error", "Error": serializer.errors})
    
    # Xóa thông tin chi tiết hóa đơn
    @api_view(['DELETE'])
    def delete_ticketdetail(request, pk):
        try:
            ticketdetail = Ticket_Import_Detail.objects.get(pk=pk)
            ticketdetail.delete()

            return Response({"Message": "success"})
        except Exception as e:
            return Response({"Message": "error", "Error": str(e)})
        
    @api_view(['GET'])
    def ticketdetail_by_ticket_id(request, pk):
        queryset = Ticket_Import_Detail.objects.filter(ticket_import = pk).select_related('product')
        orderdt = []

        for odt in queryset:
            orderdt.append({"quantity": odt.quantity,  "product_name": odt.product.product_name, "product_id": odt.product.id, 'ticket_import_id': odt.ticket_import.pk})

        return Response(orderdt)
# ===============================================================================


# ================================ API PRODUCT ==================================
class ProductView():
    # Tạo sản phẩm mới
    @api_view(['POST'])
    def create_product(request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=404)
        
    # Lấy thông tin sản phẩm theo ID
    @api_view(['GET'])
    def product_by_id(request, pk):
        try:
            prd = Product.objects.get(pk=pk)
            serializer = ProductSerializer(prd)
            return Response(serializer.data)
        except Exception as e:
            return Response(serializer.errors)
    
    # Lấy danh sách sản phẩm
    @api_view(['GET'])
    def list_product(request):
        queryset = Product.objects.select_related("branch", "category")
        print(queryset)
        products = []

        for prd in queryset:
            products.append({"id": prd.id, "branch": prd.branch.branch_name, "category": prd.category.category_name, "product_name": prd.product_name,
                            "quantity": prd.quantity, "price": prd.price, "sale": prd.sale, "rate": prd.rate, "description": prd.description,
                            "content": prd.content, "status": prd.status, "create_date": prd.create_date, "create_by": prd.create_by.username,
                            "update_date": prd.update_date, "update_by": prd.update_by.username})
        
        return Response(products)

    # Lấy danh sách sản phẩm trong trang home
    @api_view(['GET'])
    def list_product_home(request):
        list_product_home = Product.objects.raw("SELECT * FROM core_product limit 0, 16")
        data = ProductSerializer(list_product_home, many=True).data

        return Response(data)
    
    # Lấy danh sách sản phẩm trong trang shop
    @api_view(['GET'])
    def list_product_shop(request):
        list_product_shop = Product.objects.raw("SELECT * FROM core_product limit 0, 15")
        data = ProductSerializer(list_product_shop, many=True).data

        return Response(data)
    
    # Cập nhật thông tin sản phẩm
    @api_view(['PUT'])
    def update_product(request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "success", "Data": serializer.data})

        else:
            return Response({"Message": "error", "Error": serializer.errors})

    # Xóa thông tin sản phẩm
    @api_view(['DELETE'])
    def delete_product(request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.status = 0
            product.save()
        
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'error': str(e)})
        
    # Tìm kiếm thông tin sản phẩm
    @api_view(['GET'])
    def search_product(request):
        keyword = request.GET.get('keyword', '')
        product_list = Product.objects.filter(
            QuerySet(product_name__icontains=keyword)|
            QuerySet(category__icontains=keyword)
        )
        data = ProductSerializer(product_list, many=True).data
        
        return Response(data)
    
    # Lọc sản phẩm
    @api_view(['GET'])
    def filter_product(request):
        PAGE_SIZE = 5
        params = request.GET
        branch = params.get('branch_id', '').strip()
        category = params.get('category_id', '')
        
        branch = branch.split(',') if branch else []
        category = category.split(',') if category else []
        
        product_list = Product.objects.filter(category__in=category) | Product.objects.filter(branch__in =branch)

        items = product_list
        serializer = ProductSerializer(items, many=True)
        
        return Response({
            'item': serializer.data    
        })
# ===============================================================================


# ============================ API PRODUCT DETAIL ===============================
class ProductDetailView():
    # Tạo một thông tin sản phẩm chi tiết
    @api_view(['POST'])
    def create_productdetail(request):
        serializer = ProductDetailSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=404)
    
    # Cập nhật thông tin sản phẩm chi tiết
    @api_view(['PUT'])
    def update_productdetail(request, pk):
        productdt = Product_Detail.objects.get(pk=pk)
        serializer = ProductDetailSerializer(productdt, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "success", "Data": serializer.data})
        else:
            return Response({"Message": "error", "Error": serializer.errors})

    # Xóa chi tiết sản phẩm
    @api_view(['DELETE'])
    def delete_productdetail(request, pk):
        try:
            productdt = Product_Detail.objects.get(pk=pk)
            productdt.delete()

            return Response({"Message": "success"})
        except Exception as e:
            return Response({"Message": "error", "Error": str(e)})
# ===============================================================================

# ============================= API COLOR =======================================
class ColorView():
    # Lấy tất cả thông tin color
    @api_view(['GET'])
    def list_color(request):
        list_color = Color.objects.all()
        serializer = ColorSerializer(list_color, many=True)

        return Response(serializer.data)
# ===============================================================================


# ============================== API SIZE =======================================
class SizeView():
    # Lấy tất cả thông tin size
    @api_view(['GET'])
    def list_size(request):
        list_size = Size.objects.all()
        serializer = SizeSerializer(list_size, many=True)
        return Response(serializer.data)
# ===============================================================================

# ================================ API ORDER ====================================
class OrderView():
    # Tạo mới hóa đơn
    @api_view(['POST'])
    def create_order(request):
        serializer = OrdersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=404)
    
    # Lấy danh sách hóa đơn theo id
    @api_view(['GET'])
    def order_by_id(request, pk):
        order = Orders.objects.get(pk=pk)
        serializer = OrdersSerializer(order, many=True)

        return Response(serializer.data)
    
    # Lấy danh sách các hóa đơn
    @api_view(['GET'])
    def list_orders(request):
        queryset = Orders.objects.all()
        orders = []

        for ord in queryset:
            orders.append({"id": ord.id, 'order_code': ord.order_code, 'customer_name': ord.customer_name.username,
                        'phone': ord.phone, 'email': ord.email, 'address': ord.address, 'total_price': ord.total_price, 'status': ord.status, 'create_date': ord.create_date})

        return Response(orders)

    # Tìm kiếm thông tin hóa đơn
    @api_view(['GET'])
    def search_orders(self, request):
        params = request.GET
        keyword = params.get('keyword', '')
        order = Orders.objects.filter(
            QuerySet(order_code__icontains=keyword) | 
            QuerySet(customer_name__icontains = keyword) | 
            QuerySet(phone__icontains=keyword)
            )
        serializer = OrderItemlSerializer(order, many=True)
        
        return Response(serializer.data)
    

    # Cập nhật thông tin hóa đơn
    @api_view(['PUT'])
    def update_orders(request, pk):
        order = Orders.objects.get(pk=pk)
        serializer = OrdersSerializer(order, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "success", "Data": serializer.data})
        
        else:
            return Response({"Message": "error", "Error": serializer.errors})

    # Xóa thông tin hóa đơn
    @api_view(['DELETE'])
    def delete_orders(request, pk):
        try:
            orders = Orders.objects.get(pk=pk)
            orders.status = 0

            orders.save()
            return Response({"Message": "success"})
        except Exception as e:
            return Response({"Message": "error", "Error": str(e)})
# ===============================================================================

# ================================ API ORDER DETAIL =============================
class OrdersDetailView():
    # Tạo mới chi tiết hóa đơn
    @api_view(['POST'])
    def create_orderdetail(request):
        serializer = OrderItemlSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=404)
    
    # Cập nhật chi tiết hóa đơn
    @api_view(['PUT'])
    def update_orderdetail(request, pk):
        orderdt = Orders_Item.objects.get(pk=pk)
        serializer = OrderItemlSerializer(orderdt, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({"Message": "success", "Data": serializer.data})
        else:
            return Response({"Message": "error", "Error": serializer.errors})

    # Xóa thông tin chi tiết hóa đơn
    @api_view(['DELETE'])
    def delete_orderdetail(request, pk):
        try:
            orderitem = Orders_Item.objects.get(pk=pk)
            orderitem.delete()

            return Response({"Message": "success"})
        except Exception as e:
            return Response({"Message": "error", "Error": str(e)})
    
    # Lấy danh sách chi tiết hóa đơn theo id
    @api_view(['GET'])
    def getlist_orderitemby_id(request, pk):
        queryset = Orders_Item.objects.filter(order = pk).select_related('product')
        orderdt = []

        for odt in queryset:
            orderdt.append({"quantity": odt.quantity, "price": odt.price, "product": odt.product.product_name, 'order_id': odt.order.pk})

        return Response(orderdt)
# ===============================================================================