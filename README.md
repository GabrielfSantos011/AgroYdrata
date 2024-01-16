# ( AgroYdrata ) Sistema de Estimativa de Demanda de Água para Agricultura Sustentável
Sistema de Estimativa de Demanda de Água para Agricultura Sustentável
Este sistema utiliza análise de dados e aprendizado de máquina para estimar a demanda anual de água necessária para a irrigação de diferentes culturas agrícolas, contribuindo para uma gestão mais eficiente dos recursos hídricos.


# Principais Funcionalidades:
__Estimativa de Demanda de Água:__ Utiliza o algoritmo GradientBoostingRegressor, treinado com um extenso dataset, para prever a quantidade anual de água necessária com base em dados do solo, como níveis de nutrientes, temperatura, umidade, precipitação e tipo de planta.

__Histórico e Relatórios:__ Permite aos usuários visualizar o histórico de predições, filtrar por tipo de planta e gerar relatórios em PDF com detalhes das estimativas.

__Cadastro e Login:__ Funcionalidades de cadastro e login proporcionam aos usuários uma experiência personalizada.

# Tecnologias Utilizadas:

__Django e Python:__ Framework web e linguagem de programação utilizados para criar a aplicação, integrando eficientemente o frontend e o backend.

__HTML e CSS:__ Utilizados na construção e estilização das páginas da aplicação, proporcionando uma interface intuitiva.

__GradientBoostingRegressor (scikit-learn):__ Algoritmo de aprendizado de máquina utilizado para realizar as predições com base nos dados do dataset.

__Banco de Dados MySQL:__ Armazena dados do cadastro de usuários e predições realizadas.

__Bibliotecas como scikit-learn, Xhtml2pdf, Pandas e Numpy:__ Contribuem para a análise de dados, manipulação e geração de documentos PDF.

