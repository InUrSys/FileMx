'''
Created on 04/04/2018

@author: chernomirdinmacuvele
'''

table_Main_scrpts = {
        "tbl_doctype":  ["""CREATE TABLE IF NOT EXISTS doctype (cod TEXT NOT NULL PRIMARY KEY, nome TEXT NOT NULL);""",
                        [ "INSERT INTO doctype VALUES('FCT', 'Factura');",
                         "INSERT INTO doctype VALUES('RCB', 'Recibo');",
                          "INSERT INTO doctype VALUES('CV', 'Curriculum Vitae');",
                          "INSERT INTO doctype VALUES('CRT', 'Certificado');",
                          "INSERT INTO doctype VALUES('DOC', 'Documento');",
                          "INSERT INTO doctype VALUES('MST', 'Mistura');",
                          "INSERT INTO doctype VALUES('OUT', 'Outros');"
                        ]],
            
        "tbl_docfile":  ["""
                        CREATE TABLE IF NOT EXISTS docfile (
                        cod INTEGER NOT NULL,
                        cod_type TEXT NOT NULL,
                        path_file TEXT NOT NULL,
                        data_file TEXT,
                        info_file TEXT,
                        PRIMARY KEY(cod),
                        FOREIGN KEY (cod_type) REFERENCES doctype (cod)
                        ON DELETE SET NULL ON UPDATE CASCADE);
                        """,None]
        }


table_query_scrpts = {
                    'viewQuery':"""
                                SELECT tbl1.cod, tbl2.nome as "Categoria do Doc.", path_file, data_file as "Data da Imp.", info_file
                                FROM docfile as tbl1
                                inner join doctype as tbl2 
                                on  tbl1.cod_type = tbl2.cod
                                ORDER by data_file, cod_type
                                """,
                                
                    'DocTypes': """
                                SELECT null as id, '-Categoria do documento-' as nome union all  
                                SELECT cod, nome FROM doctype;
                                """
                    }

#Create DBConfiguracao
def getTableMainQueries(tblWithQuerIWant=None):
    quer = table_Main_scrpts.get(tblWithQuerIWant)
    return quer
