from rest_framework import serializers
from accounts.models import Account
from Api.models import Patient, Doctor, Sugar_level, Email



class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'age', 'phone_number', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class AccountGetSerializer(AccountCreateSerializer):
    profile_display = serializers.CharField(source='get_profile_display')

    class Meta(AccountCreateSerializer.Meta):
        fields =[]

        for field in AccountCreateSerializer.Meta.fields:
            if field == 'profile':
                fields.append('profile_display')
            elif field not in ['profile', 'password']:
                fields.append(field)



class PatientDetailsSerializer(serializers.ModelSerializer):
    user = AccountGetSerializer(many=False)

    class Meta:
        model = Patient
        fields = ('user')
#
#
# class DoctorSerializer(serializers.ModelSerializer):
#     patient = PatientDetailsSerializer(many=True)
#
#     class Meta:
#         model = Doctor
#         fields = ('descript', 'id', 'patient')
#
#
# class DoctorMinSerializer(serializers.ModelSerializer):
#     user = UserSerializer(many=False)
#
#     class Meta:
#         model = Doctor
#         fields = ('descript', 'id', 'user')
#
#
# class PatientSerializer(serializers.ModelSerializer):
#     doctor = DoctorMinSerializer(many=False)
#     user = UserSerializer(many=False)
#     all_sugar = SugarLevelSerializer(many=True)
#
#     class Meta:
#         model = Patient
#         fields = ('user', 'id', 'doctor', 'avg_sugar', 'avg_sugar_10', "avg_no_meal", 'all_sugar')
#         depth = 1
#
#
# class EmailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Email
#         fields = '__all__'

# class SugarLevelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sugar_level
#         exclude = ['patient', 'id']