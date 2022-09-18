from datetime import date
import streamlit as st
import pandas as pd
import altair
import requests

st.set_page_config(initial_sidebar_state="expanded")


def get_countries():
    url = 'http://api.worldbank.org/v2/sources/' + str(source_id) + '/country/data?format=json&per_page=1000'
    response = requests.get(url)
    data = response.json()
    return data

def get_data(country_id, country_dropdown):
    url = 'http://api.worldbank.org/v2/sources/' + str(source_id) + '/country/' + str(country_id[0]) + '/series/' + indicator_id + '/data?format=json&per_page=5000'
    response = requests.get(url)
    data = response.json()
    master_list=[]
    for item in data['source']['data']:
        for variable in item['variable']:
            if variable['concept']=='Time':
                item_list=[country_dropdown, item['value'], variable['value'], date(int(variable['value']),6,30)]
        master_list.append(item_list)
    df = pd.DataFrame(master_list, columns=['Country','Value','Year','Date'])
    return df

#Get indicator topics
@st.cache
def get_topics():
    url = "http://api.worldbank.org/v2/topic?format=json"
    response = requests.get(url)
    data = response.json()[1]
    return data
    
#Populate indicator/income dropdowns and exclude indicators that are not able to be queried from the API
@st.cache 
def get_indicators():
    indicators_exclude=['EA.PRD.AGRI.KD','EG.NSF.ACCS.RU.ZS','SH.H2O.SAFE.RU.ZS','SH.STA.ACSN.RU','SI.POV.RUGP','SI.POV.RUHC','SL.EMP.INSV.FE.ZS','SL.ISV.IFRM.FE.ZS','SL.ISV.IFRM.MA.ZS','SL.ISV.IFRM.ZS','SL.MNF.WAGE.FM','SL.TLF.PART.TL.FE.ZS','SL.TLF.PRIM.FE.ZS','SL.TLF.PRIM.MA.ZS','SL.TLF.PRIM.ZS','SL.TLF.SECO.FE.ZS','SL.TLF.SECO.MA.ZS','SL.TLF.SECO.ZS','SL.TLF.TERT.FE.ZS','SL.TLF.TERT.MA.ZS','SL.TLF.TERT.ZS','SL.UEM.LTRM.FE.ZS','SL.UEM.LTRM.MA.ZS','SL.UEM.LTRM.ZS','SL.UEM.PRIM.FE.ZS','SL.UEM.PRIM.MA.ZS','SL.UEM.PRIM.ZS','SL.UEM.SECO.FE.ZS','SL.UEM.SECO.MA.ZS','SL.UEM.TERT.FE.ZS','SL.UEM.TERT.ZS','SI.POV.2DAY','SI.POV.GAP2','SI.POV.NAGP','SI.POV.RUGP','SI.POV.RUHC','SI.POV.URGP','SI.POV.URHC','SI.SPR.PC40.05','SI.SPR.PCAP.05','IC.EXP.COST.CD','IC.EXP.DOCS','IC.EXP.DURS','IC.IMP.COST.CD','IC.IMP.DOCS','IC.IMP.DURS',
    'IE.PPI.TELE.CD','IQ.WEF.CUST.XQ','SG.JOB.NOPN.EQ','SG.LAW.CHMR','SG.LAW.LEVE.PU','SG.MMR.LEVE.EP','SG.NOD.CONS','VC.PKP.TOTL.UN','SL.EMP.INSV.FE.ZS','EG.NSF.ACCS.UR.ZS','SH.H2O.SAFE.UR.ZS','SH.STA.ACSN.UR','SI.POV.URGP','SI.POV.URHC','SG.JOB.NOPN.EQ','SG.LAW.CHMR','SG.LAW.LEVE.PU','SG.MMR.LEVE.EP','SG.NOD.CONS','SL.EMP.INSV.FE.ZS','SL.MNF.WAGE.FM','SL.TLF.PART.TL.FE.ZS','SL.TLF.PRIM.FE.ZS','SL.TLF.PRIM.MA.ZS','SL.TLF.SECO.FE.ZS','SL.TLF.SECO.MA.ZS','SL.TLF.TERT.FE.ZS','SL.TLF.TERT.MA.ZS','SL.UEM.LTRM.FE.ZS','SL.UEM.LTRM.MA.ZS','SL.UEM.PRIM.FE.ZS','SL.UEM.PRIM.MA.ZS','SL.UEM.SECO.FE.ZS','SL.UEM.SECO.MA.ZS','SL.UEM.TERT.FE.ZS','WP_time_01.2','WP_time_01.3','WP15163_4.2','WP15163_4.3','SH.H2O.SAFE.RU.ZS','SH.H2O.SAFE.UR.ZS','SH.H2O.SAFE.ZS','SH.MLR.INCD','SH.STA.ACSN','DT.DIS.IDAG.CD','DT.DOD.MDRI.CD',
    'SH.STA.ACSN','BX.GRT.EXTA.CD.DT','BX.GRT.TECH.CD.DT','BX.KLT.DINV.CD.DT','BX.KLT.DREM.CD.DT','BX.PEF.TOTL.CD.DT','DT.AMT.BLAT.CD','DT.AMT.BLAT.GG.CD','DT.AMT.BLAT.OPS.CD','DT.AMT.BLAT.PRVG.CD','DT.AMT.BLAT.PS.CD','DT.AMT.BLTC.CD','DT.AMT.BLTC.GG.CD','DT.AMT.BLTC.OPS.CD','DT.AMT.BLTC.PRVG.CD','DT.AMT.BLTC.PS.CD','DT.AMT.DEGG.CD','DT.AMT.DEPS.CD','DT.AMT.DIMF.CD','DT.AMT.DLTF.CD','DT.AMT.DLXF.CD','DT.AMT.DOPS.CD','DT.AMT.DPNG.CD','DT.AMT.DPPG.CD','DT.AMT.MIBR.CD','DT.AMT.MIDA.CD','DT.AMT.MLAT.CD','DT.AMT.MLAT.GG.CD','DT.AMT.MLAT.OPS.CD','DT.AMT.MLAT.PRVG.CD','DT.AMT.MLAT.PS.CD','DT.AMT.MLTC.CD','DT.AMT.MLTC.GG.CD','DT.AMT.MLTC.OPS.CD','DT.AMT.MLTC.PRVG.CD','DT.AMT.MLTC.PS.CD','DT.AMT.OFFT.CD','DT.AMT.OFFT.GG.CD','DT.AMT.OFFT.OPS.CD','DT.AMT.OFFT.PRVG.CD','DT.AMT.OFFT.PS.CD','DT.AMT.PBND.CD','DT.AMT.PBND.GG.CD',
    'DT.AMT.PBND.OPS.CD','DT.AMT.PBND.PRVG.CD','DT.AMT.PBND.PS.CD','DT.AMT.PCBK.CD','DT.AMT.PCBK.GG.CD','DT.AMT.PCBK.OPS.CD','DT.AMT.PCBK.PRVG.CD','DT.AMT.PCBK.PS.CD','DT.AMT.PNGB.CD','DT.AMT.PNGC.CD','DT.AMT.PROP.CD','DT.AMT.PROP.GG.CD','DT.AMT.PROP.OPS.CD','DT.AMT.PROP.PRVG.CD','DT.AMT.PROP.PS.CD','DT.AMT.PRPG.CD','DT.AMT.PRVT.CD','DT.AMT.PRVT.GG.CD','DT.AMT.PRVT.OPS.CD','DT.AMT.PRVT.PRVG.CD','DT.AMT.PRVT.PS.CD','DT.AXA.DPPG.CD','DT.AXA.OFFT.CD','DT.AXA.PRVT.CD','DT.AXF.DPPG.CD','DT.AXR.DPPG.CD','DT.AXR.OFFT.CD','DT.AXR.PRVT.CD','DT.COM.BLAT.CD','DT.COM.DPPG.CD','DT.COM.MIBR.CD','DT.COM.MIDA.CD','DT.COM.MLAT.CD','DT.COM.OFFT.CD','DT.COM.PRVT.CD','DT.CUR.DMAK.ZS','DT.CUR.EURO.ZS','DT.CUR.FFRC.ZS','DT.CUR.JYEN.ZS','DT.CUR.MULC.ZS','DT.CUR.OTHC.ZS','DT.CUR.SDRW.ZS','DT.CUR.SWFR.ZS','DT.CUR.UKPS.ZS','DT.CUR.USDL.ZS',
    'DT.DFR.DPPG.CD','DT.DIS.BLAT.CD','DT.DIS.BLAT.GG.CD','DT.DIS.BLAT.OPS.CD','DT.DIS.BLAT.PRVG.CD','DT.DIS.BLAT.PS.CD','DT.DIS.BLTC.CD','DT.DIS.BLTC.GG.CD','DT.DIS.BLTC.OPS.CD','DT.DIS.BLTC.PRVG.CD','DT.DIS.BLTC.PS.CD','DT.DIS.DEGG.CD','DT.DIS.DEPS.CD','DT.DIS.DIMF.CD','SH.MLR.INCD','SH.STA.ACSN','DT.DIS.IDAG.CD','DT.DOD.MDRI.CD','SH.STA.ACSN','BX.GRT.EXTA.CD.DT','BX.GRT.TECH.CD.DT','BX.KLT.DINV.CD.DT','BX.KLT.DREM.CD.DT','BX.PEF.TOTL.CD.DT','DT.AMT.BLAT.CD','DT.AMT.BLAT.GG.CD','DT.AMT.BLAT.OPS.CD','DT.AMT.BLAT.PRVG.CD','DT.AMT.BLAT.PS.CD','DT.AMT.BLTC.CD','DT.AMT.BLTC.GG.CD','DT.AMT.BLTC.OPS.CD','DT.AMT.BLTC.PRVG.CD','DT.AMT.BLTC.PS.CD','DT.AMT.DEGG.CD','DT.AMT.DEPS.CD','DT.AMT.DIMF.CD','DT.AMT.DLTF.CD','DT.AMT.DLXF.CD','DT.AMT.DOPS.CD','DT.AMT.DPNG.CD','DT.AMT.DPPG.CD','DT.AMT.MIBR.CD','DT.AMT.MIDA.CD',
    'DT.AMT.MLAT.CD','DT.AMT.MLAT.GG.CD','DT.AMT.MLAT.OPS.CD','DT.AMT.MLAT.PRVG.CD','DT.AMT.MLAT.PS.CD','DT.AMT.MLTC.CD','DT.AMT.MLTC.GG.CD','DT.AMT.MLTC.OPS.CD','DT.AMT.MLTC.PRVG.CD','DT.AMT.MLTC.PS.CD','DT.AMT.OFFT.CD','DT.AMT.OFFT.GG.CD','DT.AMT.OFFT.OPS.CD','DT.AMT.OFFT.PRVG.CD','DT.AMT.OFFT.PS.CD','DT.AMT.PBND.CD','DT.AMT.PBND.GG.CD','DT.AMT.PBND.OPS.CD','DT.AMT.PBND.PRVG.CD','DT.AMT.PBND.PS.CD','DT.AMT.PCBK.CD','DT.AMT.PCBK.GG.CD','DT.AMT.PCBK.OPS.CD','DT.AMT.PCBK.PRVG.CD','DT.AMT.PCBK.PS.CD','DT.AMT.PNGB.CD','DT.AMT.PNGC.CD','DT.AMT.PROP.CD','DT.AMT.PROP.GG.CD','DT.AMT.PROP.OPS.CD','DT.AMT.PROP.PRVG.CD','DT.AMT.PROP.PS.CD','DT.AMT.PRPG.CD','DT.AMT.PRVT.CD','DT.AMT.PRVT.GG.CD','DT.AMT.PRVT.OPS.CD','DT.AMT.PRVT.PRVG.CD','DT.AMT.PRVT.PS.CD','DT.AXA.DPPG.CD','DT.AXA.OFFT.CD','DT.AXA.PRVT.CD','DT.AXF.DPPG.CD',
    'DT.AXR.DPPG.CD','DT.AXR.OFFT.CD','DT.AXR.PRVT.CD','DT.COM.BLAT.CD','DT.COM.DPPG.CD','DT.COM.MIBR.CD','DT.COM.MIDA.CD','DT.COM.MLAT.CD','DT.COM.OFFT.CD','DT.COM.PRVT.CD','DT.CUR.DMAK.ZS','DT.CUR.EURO.ZS','DT.CUR.FFRC.ZS','DT.CUR.JYEN.ZS','DT.CUR.MULC.ZS','DT.CUR.OTHC.ZS','DT.CUR.SDRW.ZS','DT.CUR.SWFR.ZS','DT.CUR.UKPS.ZS','DT.CUR.USDL.ZS','DT.DFR.DPPG.CD','DT.DIS.BLAT.CD','DT.DIS.BLAT.GG.CD','DT.DIS.BLAT.OPS.CD','DT.DIS.BLAT.PRVG.CD','DT.DIS.BLAT.PS.CD','DT.DIS.BLTC.CD','DT.DIS.BLTC.GG.CD','DT.DIS.BLTC.OPS.CD','DT.DIS.BLTC.PRVG.CD','DT.DIS.BLTC.PS.CD','DT.DIS.DEGG.CD','DT.DIS.DEPS.CD','DT.DIS.DIMF.CD','DT.DIS.DLTF.CD','DT.DIS.DLXF.CD','DT.DIS.DOPS.CD','DT.DIS.DPNG.CD','DT.DIS.DPPG.CD','DT.DIS.IDAG.CD','DT.DIS.MIBR.CD','DT.DIS.MIDA.CD','DT.DIS.MLAT.CD','DT.DIS.MLAT.GG.CD','DT.DIS.MLAT.OPS.CD','DT.DIS.MLAT.PRVG.CD',
    'DT.DIS.MLAT.PS.CD','DT.DIS.MLTC.CD','DT.DIS.MLTC.GG.CD','DT.DIS.MLTC.OPS.CD','DT.DIS.MLTC.PRVG.CD','DT.DIS.MLTC.PS.CD','DT.DIS.OFFT.CD','DT.DIS.OFFT.GG.CD','DT.DIS.OFFT.OPS.CD','DT.DIS.OFFT.PRVG.CD','DT.DIS.OFFT.PS.CD','DT.DIS.PBND.CD','DT.DIS.PBND.GG.CD','DT.DIS.PBND.OPS.CD','DT.DIS.PBND.PRVG.CD','DT.DIS.PBND.PS.CD','DT.DIS.PCBK.CD','DT.DIS.PCBK.GG.CD','DT.DIS.PCBK.OPS.CD','DT.DIS.PCBK.PRVG.CD','DT.DIS.PCBK.PS.CD','DT.DIS.PNGB.CD','DT.DIS.PNGC.CD','DT.DIS.PROP.CD','DT.DIS.PROP.GG.CD','DT.DIS.PROP.OPS.CD','DT.DIS.PROP.PRVG.CD','DT.DIS.PROP.PS.CD','DT.DIS.PRPG.CD','DT.DIS.PRVT.CD','DT.DIS.PRVT.GG.CD','DT.DIS.PRVT.OPS.CD','DT.DIS.PRVT.PRVG.CD','DT.DIS.PRVT.PS.CD','DT.DOD.ALLC.CD','DT.DOD.ALLC.ZS','DT.DOD.BLAT.CD','DT.DOD.BLAT.GG.CD','DT.DOD.BLAT.OPS.CD','DT.DOD.BLAT.PRVG.CD','DT.DOD.BLAT.PS.CD','DT.DOD.BLTC.CD',
    'DT.DOD.BLTC.GG.CD','DT.DOD.BLTC.OPS.CD','DT.DOD.BLTC.PRVG.CD','DT.DOD.BLTC.PS.CD','DT.DOD.DECT.CD.CG','DT.DOD.DECT.EX.ZS','DT.DOD.DEGG.CD','DT.DOD.DEPS.CD','DT.DOD.DOPS.CD','DT.DOD.DSDR.CD','DT.DOD.MDRI.CD','DT.DOD.MLAT.CD','DT.DOD.MLAT.GG.CD','DT.DOD.MLAT.OPS.CD','DT.DOD.MLAT.PRVG.CD','DT.DOD.MLAT.PS.CD','DT.DOD.MLAT.ZS','DT.DOD.MLTC.CD','DT.DOD.MLTC.GG.CD','DT.DOD.MLTC.OPS.CD','DT.DOD.MLTC.PRVG.CD','DT.DOD.MLTC.PS.CD','DT.DOD.OFFT.CD','DT.DOD.OFFT.GG.CD','DT.DOD.OFFT.OPS.CD','DT.DOD.OFFT.PRVG.CD','DT.DOD.OFFT.PS.CD','DT.DOD.PBND.CD','DT.DOD.PBND.GG.CD','DT.DOD.PBND.OPS.CD','DT.DOD.PBND.PRVG.CD','DT.DOD.PBND.PS.CD','DT.DOD.PCBK.CD','DT.DOD.PCBK.GG.CD','DT.DOD.PCBK.OPS.CD','DT.DOD.PCBK.PRVG.CD','DT.DOD.PCBK.PS.CD','DT.DOD.PNGB.CD','DT.DOD.PNGC.CD','DT.DOD.PROP.CD','DT.DOD.PROP.GG.CD','DT.DOD.PROP.OPS.CD',
    'DT.DOD.PROP.PRVG.CD','DT.DOD.PROP.PS.CD','DT.DOD.PRPG.CD','DT.DOD.PRVS.CD','DT.DOD.PRVT.CD','DT.DOD.PRVT.GG.CD','DT.DOD.PRVT.OPS.CD','DT.DOD.PRVT.PRVG.CD','DT.DOD.PRVT.PS.CD','DT.DOD.PUBS.CD','DT.DOD.RSDL.CD','DT.DOD.VTOT.CD','DT.DSB.DPPG.CD','DT.DSF.DPPG.CD','DT.DXR.DPPG.CD','DT.GPA.DPPG','DT.GPA.OFFT','DT.GPA.PRVT','DT.GRE.DPPG','DT.GRE.OFFT','DT.GRE.PRVT','DT.INR.DPPG','DT.INR.OFFT','DT.INR.PRVT','DT.INT.BLAT.CD','DT.INT.BLAT.GG.CD','DT.INT.BLAT.OPS.CD','DT.INT.BLAT.PRVG.CD','DT.INT.BLAT.PS.CD','DT.INT.BLTC.CD','DT.INT.BLTC.GG.CD','DT.INT.BLTC.OPS.CD','DT.INT.BLTC.PRVG.CD','DT.INT.BLTC.PS.CD','DT.INT.DECT.CD','DT.INT.DECT.EX.ZS','DT.INT.DECT.GN.ZS','DT.INT.DEGG.CD','DT.INT.DEPS.CD','DT.INT.DIMF.CD','DT.INT.DLXF.CD','DT.INT.DOPS.CD','DT.INT.DPNG.CD','DT.INT.DPPG.CD','DT.INT.DSTC.CD','DT.INT.MIBR.CD',
    'DT.INT.MIDA.CD','DT.INT.MLAT.CD','DT.INT.MLAT.GG.CD','DT.INT.MLAT.OPS.CD','DT.INT.MLAT.PRVG.CD','DT.INT.MLAT.PS.CD','DT.INT.MLTC.CD','DT.INT.MLTC.GG.CD','DT.INT.MLTC.OPS.CD','DT.INT.MLTC.PRVG.CD','DT.INT.MLTC.PS.CD','DT.INT.OFFT.CD','DT.INT.OFFT.GG.CD','DT.INT.OFFT.OPS.CD','DT.INT.OFFT.PRVG.CD','DT.INT.OFFT.PS.CD','DT.INT.PBND.CD','DT.INT.PBND.GG.CD','DT.INT.PBND.OPS.CD','DT.INT.PBND.PRVG.CD','DT.INT.PBND.PS.CD','DT.INT.PCBK.CD','DT.INT.PCBK.GG.CD','DT.INT.PCBK.OPS.CD','DT.INT.PCBK.PRVG.CD','DT.INT.PCBK.PS.CD','DT.INT.PNGB.CD','DT.INT.PNGC.CD','DT.INT.PROP.CD','DT.INT.PROP.GG.CD','DT.INT.PROP.OPS.CD','DT.INT.PROP.PRVG.CD','DT.INT.PROP.PS.CD','DT.INT.PRPG.CD','DT.INT.PRVT.CD','DT.INT.PRVT.GG.CD','DT.INT.PRVT.OPS.CD','DT.INT.PRVT.PRVG.CD','DT.INT.PRVT.PS.CD','DT.IXA.DPPG.CD','DT.IXA.DPPG.CD.CG','DT.IXA.OFFT.CD',
    'DT.IXA.PRVT.CD','DT.IXF.DPPG.CD','DT.IXR.DPPG.CD','DT.IXR.OFFT.CD','DT.IXR.PRVT.CD','DT.MAT.DPPG','DT.MAT.OFFT','DT.MAT.PRVT','DT.NFL.BLAT.GG.CD','DT.NFL.BLAT.OPS.CD','DT.NFL.BLAT.PRVG.CD','DT.NFL.BLAT.PS.CD','DT.NFL.BLTC.CD','DT.NFL.BLTC.GG.CD','DT.NFL.BLTC.OPS.CD','DT.NFL.BLTC.PRVG.CD','DT.NFL.BLTC.PS.CD','DT.NFL.DECT.CD','DT.NFL.DEGG.CD','DT.NFL.DEPS.CD','DT.NFL.DLXF.CD','DT.NFL.DOPS.CD','DT.NFL.DPPG.CD','DT.NFL.DSTC.CD','DT.NFL.MLAT.GG.CD','DT.NFL.MLAT.OPS.CD','DT.NFL.MLAT.PRVG.CD','DT.NFL.MLAT.PS.CD','DT.NFL.MLTC.CD','DT.NFL.MLTC.GG.CD','DT.NFL.MLTC.OPS.CD','DT.NFL.MLTC.PRVG.CD','DT.NFL.MLTC.PS.CD','DT.NFL.NEBR.CD','DT.NFL.OFFT.GG.CD','DT.NFL.OFFT.OPS.CD','DT.NFL.OFFT.PRVG.CD','DT.NFL.OFFT.PS.CD','DT.NFL.PBND.GG.CD','DT.NFL.PBND.OPS.CD','DT.NFL.PBND.PRVG.CD','DT.NFL.PBND.PS.CD','DT.NFL.PCBK.GG.CD',
    'DT.NFL.PCBK.OPS.CD','DT.NFL.PCBK.PRVG.CD','DT.NFL.PCBK.PS.CD','DT.NFL.PROP.GG.CD','DT.NFL.PROP.OPS.CD','DT.NFL.PROP.PRVG.CD','DT.NFL.PROP.PS.CD','DT.NFL.PRPG.CD','DT.NFL.PRVT.GG.CD','DT.NFL.PRVT.OPS.CD','DT.NFL.PRVT.PRVG.CD','DT.NFL.PRVT.PS.CD','DT.NTR.BLAT.CD','DT.NTR.BLAT.GG.CD','DT.NTR.BLAT.OPS.CD','DT.NTR.BLAT.PRVG.CD','DT.NTR.BLAT.PS.CD','DT.NTR.BLTC.CD','DT.NTR.BLTC.GG.CD','DT.NTR.BLTC.OPS.CD','DT.NTR.BLTC.PRVG.CD','DT.NTR.BLTC.PS.CD','DT.NTR.DECT.CD','DT.NTR.DEGG.CD','DT.NTR.DEPS.CD','DT.NTR.DLXF.CD','DT.NTR.DOPS.CD','DT.NTR.DPNG.CD','DT.NTR.DPPG.CD','DT.NTR.MIBR.CD','DT.NTR.MIDA.CD','DT.NTR.MLAT.CD','DT.NTR.MLAT.GG.CD','DT.NTR.MLAT.OPS.CD','DT.NTR.MLAT.PRVG.CD','DT.NTR.MLAT.PS.CD','DT.NTR.MLTC.CD','DT.NTR.MLTC.GG.CD','DT.NTR.MLTC.OPS.CD','DT.NTR.MLTC.PRVG.CD','DT.NTR.MLTC.PS.CD','DT.NTR.OFFT.CD',
    'DT.NTR.OFFT.GG.CD','DT.NTR.OFFT.OPS.CD','DT.NTR.OFFT.PRVG.CD','DT.NTR.OFFT.PS.CD','DT.NTR.PBND.CD','DT.NTR.PBND.GG.CD','DT.NTR.PBND.OPS.CD','DT.NTR.PBND.PRVG.CD','DT.NTR.PBND.PS.CD','DT.NTR.PCBK.CD','DT.NTR.PCBK.GG.CD','DT.NTR.PCBK.OPS.CD','DT.NTR.PCBK.PRVG.CD','DT.NTR.PCBK.PS.CD','DT.NTR.PNGB.CD','DT.NTR.PNGC.CD','DT.NTR.PROP.CD','DT.NTR.PROP.GG.CD','DT.NTR.PROP.OPS.CD','DT.NTR.PROP.PRVG.CD','DT.NTR.PROP.PS.CD','DT.NTR.PRPG.CD','DT.NTR.PRVT.CD','DT.NTR.PRVT.GG.CD','DT.NTR.PRVT.OPS.CD','DT.NTR.PRVT.PRVG.CD','DT.NTR.PRVT.PS.CD','DT.TDS.BLAT.CD','DT.TDS.BLAT.GG.CD','DT.TDS.BLAT.OPS.CD','DT.TDS.BLAT.PRVG.CD','DT.TDS.BLAT.PS.CD','DT.TDS.BLTC.CD','DT.TDS.BLTC.GG.CD','DT.TDS.BLTC.OPS.CD','DT.TDS.BLTC.PRVG.CD','DT.TDS.BLTC.PS.CD','DT.TDS.DEGG.CD','DT.TDS.DEPS.CD','DT.TDS.DLXF.CD','DT.TDS.DOPS.CD','DT.TDS.DPNG.CD',
    'DT.TDS.MIBR.CD','DT.TDS.MIDA.CD','DT.TDS.MLAT.GG.CD','DT.TDS.MLAT.OPS.CD','DT.TDS.MLAT.PRVG.CD','DT.TDS.MLAT.PS.CD','DT.TDS.MLTC.CD','DT.TDS.MLTC.GG.CD','DT.TDS.MLTC.OPS.CD','DT.TDS.MLTC.PRVG.CD','DT.TDS.MLTC.PS.CD','DT.TDS.OFFT.CD','DT.TDS.OFFT.GG.CD','DT.TDS.OFFT.OPS.CD','DT.TDS.OFFT.PRVG.CD','DT.TDS.OFFT.PS.CD','DT.TDS.PBND.CD','DT.TDS.PBND.GG.CD','DT.TDS.PBND.OPS.CD','DT.TDS.PBND.PRVG.CD','DT.TDS.PBND.PS.CD','DT.TDS.PCBK.CD','DT.TDS.PCBK.GG.CD','DT.TDS.PCBK.OPS.CD','DT.TDS.PCBK.PRVG.CD','DT.TDS.PCBK.PS.CD','DT.TDS.PNGB.CD','DT.TDS.PNGC.CD','DT.TDS.PROP.CD','DT.TDS.PROP.GG.CD','DT.TDS.PROP.OPS.CD','DT.TDS.PROP.PRVG.CD','DT.TDS.PROP.PS.CD','DT.TDS.PRPG.CD','DT.TDS.PRVT.CD','DT.TDS.PRVT.GG.CD','DT.TDS.PRVT.OPS.CD','DT.TDS.PRVT.PRVG.CD','DT.TDS.PRVT.PS.CD','DT.TXR.DPPG.CD','DT.UND.DPPG.CD','DT.UND.OFFT.CD',
    'DT.UND.PRVT.CD','BX.KLT.DREM.CD.DT','DT.DOD.DECT.EX.ZS','DT.INT.DECT.EX.ZS','DT.INT.DECT.GN.ZS','NE.CON.PETC.CD','NE.CON.PETC.CN','NE.CON.PETC.KD','NE.CON.PETC.KD.ZG','NE.CON.PETC.KN','NE.CON.PETC.ZS','NE.CON.TETC.CD','NE.CON.TETC.CN','NE.CON.TETC.KD','NE.CON.TETC.KD.ZG','NE.CON.TETC.KN','NE.CON.TETC.ZS','NV.SRV.TETC.CD','NV.SRV.TETC.CN','NV.SRV.TETC.KD','NV.SRV.TETC.KD.ZG','NV.SRV.TETC.KN','NV.SRV.TETC.ZS','PA.NUS.PPP.05','PA.NUS.PRVT.PP.05','SE.TER.ENRL.FE.ZS','SE.XPD.MPRM.ZS','SE.XPD.MSEC.ZS','SE.XPD.MTER.ZS','SE.XPD.MTOT.ZS','SL.TLF.PRIM.FE.ZS','SL.TLF.PRIM.MA.ZS','SL.TLF.PRIM.ZS','SL.TLF.SECO.FE.ZS','SL.TLF.SECO.MA.ZS','SL.TLF.SECO.ZS','SL.TLF.TERT.FE.ZS','SL.TLF.TERT.MA.ZS','SL.TLF.TERT.ZS','SM.EMI.TERT.ZS','EG.NSF.ACCS.RU.ZS','EG.NSF.ACCS.UR.ZS','EG.NSF.ACCS.ZS','EG.NSF.ACCS.ZS','BX.KLT.DREM.CD.DT',
    'FB.AST.LOAN.CB.P3','FB.AST.LOAN.MF.P3','FB.POS.TOTL.P5','SM.EMI.TERT.ZS','WP_time_01.1','WP_time_01.2','WP_time_01.3','WP_time_01.8','WP_time_01.9','WP_time_10.1','WP_time_10.2','WP_time_10.3','WP_time_10.4','WP_time_10.5','WP_time_10.6','WP_time_10.7','WP_time_10.8','WP_time_10.9','WP15163_4.1','WP15163_4.2','WP15163_4.3','WP15163_4.8','WP15163_4.9','SH.DTH.0514','SH.DYN.0514','SH.H2O.SAFE.RU.ZS','SH.H2O.SAFE.UR.ZS','SH.H2O.SAFE.ZS','SH.MLR.INCD','SH.STA.ACSN','SH.STA.ACSN.RU','SH.STA.ACSN.UR','SH.UHC.CONS.TO','SH.UHC.CONS.ZS','SH.VST.OUTP','SH.XPD.EXTR.ZS','SH.XPD.OOPC.TO.ZS','SH.XPD.OOPC.ZS','SH.XPD.PCAP','SH.XPD.PCAP.PP.KD','SH.XPD.PRIV.ZS','SH.XPD.PUBL','SH.XPD.PUBL.GX.ZS','SH.XPD.PUBL.ZS','SH.XPD.TOTL.ZS','SM.EMI.TERT.ZS','SN.ITK.DFCT','SP.DTH.INFR.ZS','SP.DTH.REPT.ZS','IE.PPI.TELE.CD','IE.PPN.TELE.CD',
    'IQ.WEF.PORT.XQ','IT.NET.USER.P2','IT.PRT.NEWS.P3','SH.H2O.SAFE.RU.ZS','SH.H2O.SAFE.UR.ZS','SH.H2O.SAFE.ZS']
    url = 'http://api.worldbank.org/v2/indicator?format=json&per_page=50000'
    response = requests.get(url)
    data = response.json()
    indicator_list = [item for item in data[1] if item['id'] not in indicators_exclude]
    return indicator_list


#Populate title and sidebar
st.sidebar.title("Development Indicators")
st.sidebar.text('Sourced from the World Bank')
st.sidebar.image('icon-leaf-9.jpg',width=75)
st.sidebar.subheader('Topics')
topics = get_topics()
topic_selected=st.sidebar.radio('',sorted([item['value'] for item in topics]))
topic_id_selected=[item['id'] for item in topics if item['value']==topic_selected][0]
topic_note=[item['sourceNote'] for item in topics if item['value']==topic_selected][0]
st.header(topic_selected.title())
st.write(topic_note)


#Show and retrieve IDs for indicators
st.subheader('Indicators')
indicator_list = get_indicators()
indicator_list_topic = []
for item in indicator_list:
    for topic in item['topics']:
        try:
            if str(topic['id'])==str(topic_id_selected):
                indicator_list_topic.append(item)
        except:
            pass
indicator_dropdown=st.selectbox('Select an indicator', sorted([item['name'] for item in indicator_list_topic]))
indicator_id=[item['id'] for item in indicator_list_topic if item['name']==indicator_dropdown][0]
source_id=[item['source']['id'] for item in indicator_list_topic if item['name']==indicator_dropdown][0]


#Set error handler
try:
    #Create columns for filters
    with st.container():
        col1, col2 = st.columns(2)
        #Date range filter
        with col1:
            st.subheader("Filter by")
            #Populate data table and populate country list dropdown
            country_raw = get_countries()
            country_list=sorted([country['value'] for country in country_raw['source'][0]['concept'][0]['variable']])
            # if 'World' in country_list:
            country_list_default = country_list.index('World') if 'World' in country_list else 0
            country_dropdown=st.selectbox('Country or Region',country_list,index=country_list_default)
            country_id=[country['id'] for country in country_raw['source'][0]['concept'][0]['variable'] if country['value']==country_dropdown]

    #Populate tables and graphs
    st.subheader(indicator_dropdown)
    st.text(country_dropdown)
    df_query=get_data(country_id, country_dropdown) 
    chart = altair.Chart(df_query.dropna()).mark_line().encode(altair.X('Date',title='Year'), altair.Y('Value',title='Value')).configure_mark(color='red').properties(width=800,height=300).configure_axisX(labelAngle=270)
    st.write(chart)
    st.write([item['sourceNote'] for item in indicator_list_topic if item['name']==indicator_dropdown][0])
    df_query=df_query.drop(columns=['Date'])
    st.dataframe(df_query)
except Exception as e:
    # st.write(e)
    pass
    st.text('This indicator could not be queried. Please select another.')