from rest_framework import serializers
from accounts.models import Account
from Api.models import Patient, Doctor, SugarLevel, Chat, Cooperate, Advice, RejectCooperate


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'age', 'phone_number', 'password', 'profile', 'id']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'age', 'phone_number', 'id']


class AccountGetSerializer(AccountCreateSerializer):
    profile_display = serializers.CharField(source='get_profile_display')

    class Meta(AccountCreateSerializer.Meta):
        fields = []

        for field in AccountCreateSerializer.Meta.fields:
            if field == 'profile':
                fields.append('profile_display')
            elif field not in ['profile', 'password']:
                fields.append(field)


class PatientListSerializer(serializers.ModelSerializer):
    account = AccountGetSerializer(many=False)

    class Meta:
        model = Patient
        fields = ['account', ]


class PatientDetailSerializer(PatientListSerializer):

    class Meta(PatientListSerializer.Meta):
        fields = '__all__'


class DoctorGetSerializer(serializers.ModelSerializer):
    account = AccountGetSerializer(many=False)

    class Meta:
        model = Doctor
        fields = 'account',


class DoctorListSerializer(serializers.ModelSerializer):
    account = AccountListSerializer(many=False)

    class Meta:
        model = Doctor
        fields = ['account',]


class CooperateGetSerializer(serializers.ModelSerializer):
    doctor = AccountGetSerializer(many=False)
    patient = AccountGetSerializer(many=False)
    class Meta:
        model = Cooperate
        fields = ['doctor', 'patient', 'message', 'date', 'id', 'is_active']


class CooperateNewSerializer(serializers.ModelSerializer):
    patient = AccountGetSerializer(many=False)
    class Meta:
        model = Cooperate
        fields = ['patient', 'message', 'date', 'id']


class CooperateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooperate
        fields = '__all__'


class SugarLevelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SugarLevel
        fields = ['level', 'date']


class SugarLevelGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SugarLevel
        exclude = ['account', ]

class SugarLevelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SugarLevel
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class AdviceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advice
        fields = '__all__'

class AdviceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advice
        exclude = ['patient','doctor',]

class RejectCooperateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RejectCooperate
        fields = '__all__'


class ChatNewMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['sender', 'doctorId', 'patientId']
