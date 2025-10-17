
import ee



def loaddef():
    try:

        ee.Initialize()
    except Exception as e:
        credentials = ee.ServiceAccountCredentials(
            'geeresearch@geeapp-1577771889447.iam.gserviceaccount.com', 'geeapp-1577771889447-dd8ab00048c7.json')
        ee.Initialize(credentials)



