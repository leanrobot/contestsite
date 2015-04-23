from django import forms

class ContestSettingForm(forms.ModelForm):
	class Meta:
		model = ContestSetting
		fields = ['startTime', 'endTime', 'paused']