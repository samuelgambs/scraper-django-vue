from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import datetime
import json
import time
import requests

#system hour
DT_HR_PROCESSAMENTO = time.strftime("%Y-%m-%d %H:%M")

def log_erros(item, erro, tabela):
    data_gravacao = datetime.datetime.strptime(item['data_gravacao'], '%d/%m/%Y %H:%M')

    if type(erro) is str:
        payload  = {
        "ID_CLIENTE" : 0,
        "ID_SUB_CONTA" : 0,
        "ID_USUARIO" : 0,
        "ID_WEBSERVICES_RC" : 'PROCESSA_GATEWAY',	
        "DT_HR_ERRO" : DT_HR_PROCESSAMENTO,
        "CODIGO_ERRO_BD" : 0,
        "MSG_ERRO_BD" : erro,
        "TABELA_VIEW_RELACIONADA" : tabela,
        "COMANDO_UTILIZADO" : 0,
        "JSON" : item
        }
    else:
        payload  = {
            "ID_CLIENTE" : 0,
            "ID_USUARIO" : 0,
            "ID_WEBSERVICES_RC" : 'PROCESSA_GATEWAY',	
            "DT_HR_ERRO" : DT_HR_PROCESSAMENTO,
            "CODIGO_ERRO_BD" : erro.errno,
            "MSG_ERRO_BD" : erro.msg,
            "TABELA_VIEW_RELACIONADA" : erro,
            "COMANDO_UTILIZADO" : erro.sqlstate,
            "JSON" : item
        }

    url = "http://brasiltrack.com/APP001_ERROS_IO"

    r = requests.get(url, params=payload)
    print(r.url)

    sql_insert_registro_rastreamento = """
            INSERT INTO rc.registros_de_rastreamento
            (
            ID_GATEWAY,
            DT_HR_RECEBIMENTO,
            DT_HR_PROCESSAMENTO,
            JSON_REGISTRO_DE_RASTREAMENTO)
            VALUES(
            {ID_GATEWAY},
            "{DT_HR_RECEBIMENTO}",
            "{DT_HR_PROCESSAMENTO}",
            '{JSON_REGISTRO_DE_RASTREAMENTO}')
            """.format(
            ID_GATEWAY = item['gateway_fisico'],
            DT_HR_RECEBIMENTO = data_gravacao,
            DT_HR_PROCESSAMENTO = DT_HR_PROCESSAMENTO,
            JSON_REGISTRO_DE_RASTREAMENTO = json.dumps(item))

    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(sql_insert_registro_rastreamento)
    except Error as e:
        print(e)
        print("Erro ao salvar na tabela registros_de_rastreamento")
    finally:
        cursor.close()
        conn.close()
    

with open("dados_gateway.json", encoding="utf8") as read_file:
    items = json.load(read_file)
    for item in items:
        
        #lendo tabela modulo rastreador
        sql_modulo_rastreador = """
            SELECT MODULO_RASTREADOR.ID_MODULO_RASTREADOR, 
                MODULO_RASTREADOR.ID_MODELO_RASTREADOR, 
                GATEWAY.ID_GATEWAY 
            FROM   MODULO_RASTREADOR, 
                GATEWAY 
            WHERE  MODULO_RASTREADOR.ID_ORIGINAL = {MODULO} 
                AND MODULO_RASTREADOR.ID_FABRICANTE =  {FABRICANTE}
                AND GATEWAY.ID_MODELO_MODULO_RASTREAMENTO = 
                    MODULO_RASTREADOR.ID_MODELO_RASTREADOR 
                AND GATEWAY.CODIGO_GATEWAY_FISICO = {GATEWAY}""".format(
                    MODULO = item['id2'], 
                    FABRICANTE = item['fabricante'], 
                    GATEWAY = item['gateway_fisico'] )
        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute(sql_modulo_rastreador)
            rows = cursor.fetchall()

            if not rows:
                e = "Sem registros para este item no módulo rastreador"
                log_erros(item, e, 'MODULO_RASTREADOR')
                continue

            for row in rows:
                id_modulo_rastreador = row[0]
            
        except Error as e:            
            log_erros(item, e, 'MODULO_RASTREADOR')

        finally:
            cursor.close()
            conn.close()

        #lendo tabela conjunto rastreado
        sql_conjunto_rastreado = """
        SELECT ID_CONJUNTO_RASTREADO, 
            ID_CLASSE_COISA, 
            ID_COISA, 
            ID_CLIENTE,
            ID_SUB_CONTA
            DT_HR_ULT_TRANSMISSAO
            
        FROM   CONJUNTO_RASTREADO 
        WHERE  CONJUNTO_RASTREADO.ID_MODULO_RASTREADOR = {ID_MODULO_RASTREADOR}
            AND STATUS_CONJUNTO_RASTREADO = 1 LIMIT 1
                """.format(ID_MODULO_RASTREADOR = id_modulo_rastreador)

        try:          
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute(sql_conjunto_rastreado)
            row = cursor.fetchone()

            if not row:
                e = "Sem registros para este item no CONJUNTO_RASTREADO"
                log_erros(item, e, 'CONJUNTO_RASTREADO')
                continue

            
            idcliente = row[3]
            idcoisa = row[2]
            idclassecoisa = row[1]
            id_conjunto_rastreado = row[0]
            id_sub_conta = row[4]
            dt_hr_ult_transmissao = datetime.datetime.strptime(item['data_gravacao'], '%d/%m/%Y %H:%M')

        except Error as e:
            log_erros(item, e, 'CONJUNTO_RASTREADO')
            continue
        finally:
            cursor.close()
            conn.close()
        dh_equipamento = datetime.datetime.strptime(item['dh_equipamento'], '%d/%m/%Y %H:%M')
        data_gravacao = datetime.datetime.strptime(item['data_gravacao'], '%d/%m/%Y %H:%M')    

        sql_layout_rastreamento = """
                SELECT   id_variaveis_de_rastreamento, 
                id_tipo_reg_rastreamento, 
                id_layout_reg_rastreamento, 
                status_variavel_de_rastreamento, 
                desc_variavel_de_rastreamento, 
                desc_coluna_tab_historico, 
                seq_apresentacao, 
                posicao_inicial, 
                posicao_final, 
                ind_tp_campo, 
                comando_conversao_campo, 
                qtd_bytes_inteiros, 
                qtd_bytes_decimais, 
                qtd_bytes_alfanumericos 
        FROM     variaveis_de_rastreamento 
        WHERE    variaveis_de_rastreamento.id_tipo_reg_rastreamento = {TIPO_REGISTRO}
        AND      status_variavel_de_rastreamento = 1 
        AND      id_layout_reg_rastreamento IN 
                ( 
                        SELECT 
                            MAX(id_layout_reg_rastreamento) 
                        FROM   layout_reg_rastreamento 
                        WHERE  layout_reg_rastreamento.id_tipo_reg_rastreamento = {TIPO_REGISTRO}
                        AND    layout_reg_rastreamento.dt_hr_ini_validade <= '{DH_EQUIPAMENTO}' 
                        AND    layout_reg_rastreamento.dt_hr_fim_validade >= '{DH_EQUIPAMENTO}' )
        ORDER BY variaveis_de_rastreamento.seq_apresentacao LIMIT 1""".format(
            TIPO_REGISTRO = item['tiporegistro'],
            DH_EQUIPAMENTO = dh_equipamento)


        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute(sql_layout_rastreamento)
            rows = cursor.fetchone()

            if not rows:
                e = "Sem registros para nome tabela variaveis rastreamento"
                log_erros(item, e, 'variaveis_de_rastreamento')
                continue
            
            id_variaveis_de_rastreamento = rows[0]
            id_tipo_reg_rastreamento = rows[1]
            id_layout_reg_rastreamento = rows[2]

        except Error as e:
            log_erros(item, e, 'variaveis_de_rastreamento')
            continue

        finally:
            cursor.close()
            conn.close()    


        

        #buscar o nome da tabela de histórico de rastreamento 
        sql_historico_rastreamento = """
        SELECT A.nome_tab_hst_rastreamento 
        FROM   classe_tipo_reg_rastreamento AS A, 
            conjunto_rastreado AS B 
        WHERE  A.id_classe_coisa = B.id_classe_coisa 
            AND A.id_tipo_reg_rastreamento = {registro} 
            AND A.ind_setup_ok = 1 LIMIT 1""".format(registro = item['tiporegistro'])

        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute(sql_historico_rastreamento)
            row = cursor.fetchone()

            if not rows:
                e = "Sem registros para nome tabela histórico rastreamento"
                print(e)
                log_erros(item, e, 'conjunto_rastreado')
                continue
            
            
            nome_tab_hst_rastreamento = row[0]
            nome_tab_hst_rastreamento[2:-2] 

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()    

        sql_show_columns = "SHOW columns FROM {TABLE}".format(TABLE = nome_tab_hst_rastreamento)  
        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute(sql_show_columns)
            rows = cursor.fetchall()

            if not rows:
                e = "Sem registros para nome tabela histórico "
                print(e)
                log_erros(item, e, 'tabela_historico')
                continue
            
            
        except Error as e:
            print(e)
            
        finally:
            cursor.close()
            conn.close()

        
        sql_insert_registro_rastreamento = """
        INSERT INTO registros_de_rastreamento
            (ID_CLIENTE,
            ID_COISA,
            ID_TIPO_REG_RASTREAMENTO,
            ID_GATEWAY,
            ID_LAYOUT_REG_RASTREAMENTO,
            ID_MODULO_RASTREADOR,
            DT_HR_RECEBIMENTO,
            DT_HR_PROCESSAMENTO,
            JSON_REGISTRO_DE_RASTREAMENTO)
            VALUES(
            {ID_CLIENTE},
            {ID_COISA},
            {ID_TIPO_REG_RASTREAMENTO},
            {ID_GATEWAY},
            {ID_LAYOUT_REG_RASTREAMENTO},
            {ID_MODULO_RASTREADOR},
            "{DT_HR_RECEBIMENTO}",
            "{DT_HR_PROCESSAMENTO}",
            '{JSON_REGISTRO_DE_RASTREAMENTO}')""".format(ID_CLIENTE = idcliente,
            ID_CLASSE_COISA = idclassecoisa, 
            ID_COISA = idcoisa,
            DT_HR_RECEBIMENTO = DT_HR_PROCESSAMENTO,
            DT_HR_PROCESSAMENTO = data_gravacao,
            ID_LAYOUT_REG_RASTREAMENTO = id_layout_reg_rastreamento,
            ID_TIPO_REG_RASTREAMENTO = id_tipo_reg_rastreamento,
            ID_GATEWAY = item['gateway_fisico'],
            ID_MODULO_RASTREADOR = id_modulo_rastreador,
            DT_HR_MODULO = dh_equipamento,
            JSON_REGISTRO_DE_RASTREAMENTO = json.dumps(item))

        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute(sql_insert_registro_rastreamento)
        except Error as e:
            print(e)
            log_erros(item,e,'registros_de_rastreamento')
        finally:
            cursor.close()
            conn.close()
        

        sql_id_ultimo_registro = """
            SELECT ID_REGISTRO_DE_RASTREAMENTO
            FROM registros_de_rastreamento
            WHERE ID_REGISTRO_DE_RASTREAMENTO > 1
            ORDER BY ID_REGISTRO_DE_RASTREAMENTO DESC
            LIMIT 1;"""

        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute(sql_id_ultimo_registro)
            rows = cursor.fetchall()

            if not rows:
                e = "Sem registros para registros_de_rastreamento"
                print(e)
                log_erros(item, e, 'registros_de_rastreamento')
                continue

            for row in rows:
                id_registro_de_rastreamento = row[0] 

        except Error as e:
             log_erros(item, e, 'registros_de_rastreamento')
        finally:
            cursor.close()
            conn.close()

        values = []
        row_values = []
        for row in rows:
            for field, possible_values in item.items():
                field = field.upper()
                if (field == row[0]):
                    row_values.append(row[0])
                    values.append(str(possible_values))


        #sql_dynamic_insert = "INSERT INTO {TABLE}".format(TABLE = nome_tab_hst_rastreamento) 

        """Take dictionary object dict and produce sql for 
        inserting it into the named table"""
        sql = 'INSERT INTO ' + nome_tab_hst_rastreamento
        sql += ' ( ID_REGISTRO_DE_RASTREAMENTO, ID_CLIENTE, ID_CLASSE_COISA, ID_COISA, DT_HR_RECEBIMENTO, DT_HR_PROCESSAMENTO, ID_LAYOUT_REG_RASTREAMENTO, ID_TIPO_REG_RASTREAMENTO, ID_GATEWAY, ID_MODULO_RASTREADOR, DT_HR_MODULO, VERSAO_SW, PROTOCOLO'
        sql += ', '.join(row_values)
        sql += ') VALUES (' + str(item['tiporegistro']) + ',' + str(idcliente) + ',' + str(idclassecoisa) + ',' + str(idcoisa) + ', "' 
        sql +=  str(DT_HR_PROCESSAMENTO) + '", "' + str(DT_HR_PROCESSAMENTO) +  '",' + str(id_layout_reg_rastreamento) + ',' + str(id_tipo_reg_rastreamento) + ',' 
        sql += str(item['gateway_fisico']) + ',' + str(id_conjunto_rastreado) + ',"' +  str(DT_HR_PROCESSAMENTO) + '",'
        sql += str(item['versao_sw']) + ',' + str(item['protocolo'])
        sql += ', '.join(values)
        sql += ');'


        try:
            print(sql)
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute(sql)
        except Error as e:
            print(e)
            log_erros(item,e, nome_tab_hst_rastreamento)
        finally:
            cursor.close()
            conn.close()




        for key in item.keys():
            sql_update_itens_rastreamento = """
                UPDATE itens_de_rastreamento 
                    SET    vlr_itens_de_rastreamento = "{CAMPO}", 
                        id_ult_registros_de_rastreamento = 
                         {ID_REGISTRO_RASTREAMENTO} 
                    WHERE  itens_de_rastreamento.id_variaveis_de_rastreamento = 
                                {VARIAVEIS_DE_RASTREAMENTO} 
                        AND itens_de_rastreamento.id_modulo_rastreador = 
                            {ID_MODULO_RASTREADOR} 
                        AND itens_de_rastreamento.id_tipo_reg_rastreamento = {TIPO_REGISTRO}""".format(
                            CAMPO = key,
                            TIPO_REGISTRO = item['tiporegistro'],
                            VARIAVEIS_DE_RASTREAMENTO = id_variaveis_de_rastreamento,
                            ID_MODULO_RASTREADOR = id_modulo_rastreador,
                            ID_REGISTRO_RASTREAMENTO = id_registro_de_rastreamento) 
            try:
                #print(sql_update_itens_rastreamento)
                dbconfig = read_db_config()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                cursor.execute(sql_update_itens_rastreamento)
            except Error as e:
                print(e)
            finally:
                cursor.close()
                conn.close()

        sql_update_conjunto_rastreado = """
            UPDATE conjunto_rastreado 
            SET    dt_hr_penultima_transmissao = '{DH_AUXILIAR}', 
                dt_hr_ult_transmissao = '{DT_HR_ULT_TRANSMISSAO}', 
                ind_transmissao_ok = 1 
            WHERE  id_modulo_rastreador =  {ID_MODULO_RASTREADOR}
            AND    status_conjunto_rastreado = 1""".format(
            DH_AUXILIAR = data_gravacao,
            DT_HR_ULT_TRANSMISSAO = dh_equipamento,
            ID_MODULO_RASTREADOR=id_modulo_rastreador)

        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute(sql_update_conjunto_rastreado)

        except Error as e:
            print(e)

        finally:
            cursor.close()
            conn.close()
            

        
