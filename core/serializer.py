from rest_framework import serializers
from .models import *


# ===================== USER =================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance
# ==============================================================


# ==================== SUPPLIER ================================
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"
# ===============================================================


# ==================== CATEGORY =================================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
# ===============================================================


# ======================= BRANCH ================================
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"
# ===============================================================


# ===================== TICKET IMPORT ===========================
class TicketImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket_import
        fields = "__all__"
# ===============================================================


# ====================== TICKER IMPORT DETAIL ===================
class TicketDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket_Import_Detail
        fields = "__all__"
# ===============================================================

# =================== PRODUCT ===================================
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
# ================================================================


# ======================= IMAGE =================================
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['image']          
# ===============================================================

# ========================= PRODUCT DETAIL ======================
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Detail
        fields = "__all__"
# ===============================================================


# ======================== ORDER ================================
class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"
# ===============================================================


# =========================== ORDER DETAIL ======================
class OrderItemlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders_Item
        fields = "__all__"
# ================================================================


# ======================= SIZE ===================================
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"
# =================================================================


# ======================== COLOR ==================================
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"
# ==================================================================


# ========================= USER ROLE ==============================
class UserRoleSerializer(serializers.ModelSerializer):
     class Meta:
        model = User_role
        fields = "__all__"
# ==================================================================