from os import error
from src.util.tools import tools
from src.util.database import DB

class oRpt:

    def __init__(self, params):
        self.params = params
        self.spList = ['sp_get_qualifications_data', 'sp_get_qualification_header', 'sp_get_header_cotejo_rpt', 'sp_get_cotejo_student_list', 'sp_get_cotejo_info', 'sp_get_header_aprettiationRpt', 'sp_get_aprettiation_qualificationList']
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
        if(self.params["rpt_type"] == 'ct'):
            o_CTId = []
            o_information = DB().exec_query(self.spList[4], [self.params['rpt_clist_id']])
            o_ctHeader = DB().exec_query(self.spList[2], [self.params['rpt_clist_id'], self.params['rpt_unit_number']])
            if(o_ctHeader.get('err') or o_information.get('err')):
                return{
                        'msm':'error',
                        'err':self.getInfoErr
                        }
            o_newHeader = self.MakeNewHeader(o_ctHeader.get('data'))
            for d in o_newHeader:
                o_CTId.append(d[0])
            o_Body = self.MakeoBodyCT(o_CTId) 
            return{
                    'msm':'success',
                    'o_header':o_newHeader,
                    'o_body':o_Body,
                    'o_info':o_information.get("data"),
                    'year':self.params['rpt_year']
                    }
        if(self.params["rpt_type"] == 'ap'):
            o_APinformation = DB().exec_query(self.spList[4], [self.params['rpt_clist_id']])
            o_APheader = DB().exec_query(self.spList[5], [self.params['rpt_clist_id']])
            o_APbody = DB().exec_query(self.spList[6], [self.params['rpt_listId'], self.params['rpt_clist_id']])
            if(o_APinformation.get('err') or o_APheader.get('err') or o_APbody.get('err')):
                return{
                        'msm':'error',
                        'err':self.getInfoErr
                        }
            return{
                    'msm':'success',
                    'o_header':o_APheader.get('data'),
                    'o_body':o_APbody.get('data'),
                    'o_info':o_APinformation.get('data'),
                    'year':self.params['rpt_year']
                    }

        return{
                'msm':'error',
                'err':self.defaultErr
                }

    def MakeoBodyCT(self, item:list):
        if(len(item) < 5):
            i = len(item) - 1
            while(i < 5):
                item.append(0)
                i += 1
        o_Data = DB().exec_query(self.spList[3], [item[0], item[1], item[2], item[3], item[4], self.params['rpt_clist_id'], self.params['rpt_unit_number']])
        if(o_Data.get('err')):
            return []
        return o_Data.get("data")

    def MakeNewHeader(self, item):
        if(len(item) < 5):
            i = len(item) - 1
            while(i < 5):
                item.append((0, '', 0, '', 0, '', 0))
                i += 1
        return item

