from src.util.tools import tools
from src.util.database import DB

class oRpt:

    def __init__(self, params):
        self.params = params
        self.spList = ['sp_get_qualifications_data', 'sp_get_qualification_header']
        self.getInfoErr = 'Ocurrio un error al tratar de obtener la informacion, por favor contacte a soporte de IT si el error persiste'
        self.defaultErr = 'No se encontro una variante para el reporte solicitado, por favor contacte a soporte de IT si el error persiste'

    def Get_rpt(self):
        oData = self.MakeoData()
        if(oData.get('err')):
            return oData
        return tools().consume_reportApi(oData, self.MakeoRpt())

    def MakeoRpt(self): 
        return{
                'rpt_type':self.params['rpt_type'],
                'rpt_extend_data':{}
                  }

    def MakeoData(self):
        if(self.params['rpt_type'] == 'qa'):
            o_header = DB().exec_query(self.spList[1], [self.params['rpt_student_id']])
            o_qualification = DB().exec_query(self.spList[0], [self.params['rpt_student_id'], self.params['rpt_year']])
            if(o_header.get('err') or  o_qualification.get('err')):
                return{
                        'msm':'error',
                        'err':self.getInfoErr
                        }
            return{
                    'msm':'success',
                    'q_header':o_header.get('data'),
                    'o_qualification':o_qualification.get('data')
                    }
        return{
                'msm':'error',
                'err':self.defaultErr
                }

