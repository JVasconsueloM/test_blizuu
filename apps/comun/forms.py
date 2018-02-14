from django import forms

from apps.comun.constants import SORT_GITHUB_REPOSITORIES, CREATED_DATE


class GitHubRepositoriesForm(forms.Form):
    orden = forms.ChoiceField(SORT_GITHUB_REPOSITORIES, required=False)
    busqueda = forms.CharField(max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        super(GitHubRepositoriesForm, self).__init__(*args, **kwargs)
        self.fields['orden'].widget.attrs.update({
            'class': 'form-control form-control-dark w-100 p-5 col-md-8 h-46 ',
            'placeholder': "Search"
        })
        self.fields['busqueda'].widget.attrs.update({
            'class': 'form-control form-control-dark w-100 col-md-8',
            'placeholder': "Search"
        })

    def get_params(self):
        busqueda = self.cleaned_data.get('busqueda', '')
        orden = self.cleaned_data.get('orden', CREATED_DATE)
        return {'search': busqueda, 'sort': orden}
