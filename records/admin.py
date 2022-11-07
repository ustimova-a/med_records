from django.contrib import admin
from .models import Hospital, Specialty, Physician, Condition, Drug, Document, Treatment, Visit


class HospitalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'website')


class PhysicianAdmin(admin.ModelAdmin):
    exclude = ('patronymic',)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('date_issued', 'physician', 'condition', 'prescribed_drug_list', 'source_doc')

    def prescribed_drug_list(self, document):
        return ', '.join(map(str, document.prescribed_drug.values_list('id', flat=True)))


class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('prescribed_drug_list', 'dosage', 'dosing_regimen', 'comment')

    def prescribed_drug_list(self, treatment):
        return ', '.join(map(str, treatment.prescribed_drug.values_list('id', flat=True)))


class VisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_attended', 'physician', 'hospital', 'document', 'treatment', 'comment')


admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Specialty)
admin.site.register(Physician, PhysicianAdmin)
admin.site.register(Condition)
admin.site.register(Drug)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Treatment, TreatmentAdmin)
admin.site.register(Visit, VisitAdmin)


