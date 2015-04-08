import django_tables2 as tables
from main.models import User, Person, RadiologyRecord, PacsImage, FamilyDoctor


#
class ThumbnailMixin(tables.Table):
    preview = tables.TemplateColumn(
'''
<a class="thumbnail" href="/ris/record/{{record.record_id}}/images">
    <img class="img-responsive" src="data:image/jpeg;base64,{{record.thumbnail}}" alt="no image" style="width: 50%; height: 50%">
</a>
''',
orderable=False
    )
    class Meta:
        model = PacsImage
        fields = ('preview',)


class RecordSearchTable(ThumbnailMixin, tables.Table):
    patient = tables.Column(accessor='patient.full_name', order_by=("patient.last_name",))
    doctor = tables.Column(accessor='doctor.full_name', order_by=("doctor.last_name",))
    radiologist = tables.Column(accessor='radiologist.full_name', order_by=("radiologist.last_name",))

    class Meta:
        model = RadiologyRecord
        fields = ('record_id', 'rank', 'patient', 'doctor', 'radiologist', 'test_type', 'prescribing_date', 'test_date', 'diagnosis')

        sequence = ('record_id', 'rank', 'patient', 'doctor', 'radiologist', 'test_type', 'prescribing_date', 'test_date', 'diagnosis', '...')

class EditableRecordSearchTable(RecordSearchTable):
    # TODO: It would probably be better to seperate this view from the model/controller logic..
    edit = tables.TemplateColumn(
'''
<div class="dropdown">
    <a href="#" class="dropdown-toggle" data-toggle="dropdown">Options
        <span class="caret"></span>
    </a>
    <ul class="dropdown-menu">
        <li>
            <a href="/ris/record/{{record.record_id}}/update/">Edit Record</a>
        </li>
        <li>
            <a href="/ris/images/add/?record_id={{record.record_id}}">Add Images</a>
        </li>
    </ul>
</div>
''',
orderable=False
    )

class DataCubeTable(tables.Table):
# 'Count':1L,'test_type':u'xyz','Patient':2,'test_date':'2015-03-30'
    patient = tables.Column(verbose_name="Patient ID")
    test_type = tables.Column()
    test_date = tables.Column()
    image_count = tables.Column()
