
from SaaS_DAO.Connections import Connections


class GestionSaaSDao:

    def getMembre():
        sqlnom=("select identifiant, permission,titre from 'membre'")
        tempo = Connections.getConnectionDBGestion()
        c = tempo.cursor()
        try:
            if c is not None:
                c.execute(sqlnom)
                result = tempo.fetchall()
                return result
        except:
            print("errreur getmembre")
        finally:
            c.close()
