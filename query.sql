SELECT
  PRE_MED.CD_PRE_MED,
  PACIENTE.CD_PACIENTE,
  TRUNC((PRE_MED.DT_PRE_MED - PACIENTE.DT_NASCIMENTO) / 365) AS IDADE_PACIENTE,
  PACIENTE.TP_SEXO AS SEXO,
  PRE_MED.DT_PRE_MED AS DATA_EVOLUCAO,
  CID.DS_CID ,
  PRE_MED.DS_EVOLUCAO AS EVOLUCAO,
  ATENDIME.SN_OBITO AS OBITO,
    CASE 
        WHEN ATENDIME.SN_OBITO = 'S' THEN ATENDIME.DT_ALTA
        WHEN ATENDIME.SN_OBITO = 'N' THEN NULL
        ELSE NULL 
    END AS data_obito,
  av.DT_AVISO_CIRURGIA AS DATA_AVISO_CIRURGIA,
  ci.DS_CIRURGIA AS CIRURGIA,

    CASE 
        WHEN av.CD_ASA = 'ASA I' THEN ' (Paciente saudavel)'
        WHEN av.CD_ASA = 'ASA II' THEN 'ASA II (Paciente com enfermidade sistemica leve)'
        WHEN av.CD_ASA = 'ASA III' THEN 'ASA III (Paciente com enfermidade sistemica severa)'
        WHEN av.CD_ASA = 'ASA IV' THEN 'ASA IV (Paciente com enfermidade sistemica e com risco de vida)'
        WHEN av.CD_ASA = 'ASA V' THEN 'ASA V (Paciente com expectativa de óbito antes de 24 horas)'
        WHEN av.CD_ASA = 'E' THEN 'Emergencia'
        ELSE NULL
    END AS CLASSIFICACAO_ASA,

    CASE 
        WHEN av.tp_cirurgias = 'E' THEN 'Cirurgia Eletiva'
        WHEN av.tp_cirurgias = 'M' THEN 'Emergencia'
        WHEN av.tp_cirurgias = 'U' THEN 'Urgencia'
        ELSE NULL
    END AS TIPO_CIRURGIA


FROM PRE_MED

INNER JOIN ATENDIME ON PRE_MED.CD_ATENDIMENTO = ATENDIME.CD_ATENDIMENTO
INNER JOIN PACIENTE ON ATENDIME.CD_PACIENTE = PACIENTE.CD_PACIENTE
INNER JOIN CID ON ATENDIME.cd_cid = CID.cd_cid
LEFT JOIN AVISO_CIRURGIA av ON ATENDIME.CD_ATENDIMENTO = av.CD_ATENDIMENTO AND av.TP_SITUACAO = 'R'  -- filtra para cirurgias realizadas
LEFT JOIN CIRURGIA_AVISO ca ON av.CD_AVISO_CIRURGIA = ca.CD_AVISO_CIRURGIA
LEFT JOIN CIRURGIA ci ON ca.CD_CIRURGIA = ci.CD_CIRURGIA



WHERE
  PRE_MED.cd_objeto = 409   -- Filtro evolução médica
  AND PACIENTE.CD_PACIENTE NOT IN (22849, 21290, 21340, 99999999, 21343)  -- Remover testes
  AND CID.CD_CID LIKE '%C%'




ORDER BY PACIENTE.CD_PACIENTE, PRE_MED.DT_PRE_MED;
