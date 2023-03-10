   
   Este é um projeto de software que gere automaticamente um ralatorio de um ensaio de compactação cbr        
ou marshall de acordo com as normas vigentes.
    Basicamente o porgrama recebe do usuario o tipo de ensaio desejado e em sequencia o programa recebe 
os dados de entrada do usuario (identificação do usuario e detalhes da amostra) e salva temporariamente 
em um banco de dados. Depois ele se conecta com um microcontrolador por meio de comunicação serial e o 
ensaio é realizado.
    O ensaio em si consiste em receber os valores de força e deslocamento vindos de algum microcontrolador
que recebe esses dados de sensores, durante o recebimentto dos dados ele gera para o usuario um grafico em 
tempo real de forca x deslocamento. Apos o fim do ensaio o programa pega os valores recebidos pelo usuario 
e os valores recebidos de força e deslocamento e gera um pdf que ira conter os dados recebidos do usuario
e mais alguns graficos especificos de cada ensaio além de valores criticos que são calculados com os dados
recebidos.
    Atualmente o projeto ainda não esta finalizado.
