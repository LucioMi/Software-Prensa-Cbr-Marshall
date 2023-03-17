/*
    Este é um codigo para o microcontrolador arduino que visa simular valores de entrada (força e deslocamento) com o uso de potenciometros. Para assim junto
  com o arduino poder criar simulações de funcionamento da prensa com as entradas 'analogicas'. Na vida real o sensor de força sera uma celula de carga de 
  5 toneladas e o sensor de deslocamento um LVDT de 25mm. 
    A variavel Estado que é recebida por comunicação serial controla o ensaio onde o byte 251 liga a prensa em modo marshall, o byte 252 liga a prensa em modo
  CBR o byte 253 retorna a prensa para a posição inicial (deslocamento = 0 ) e qualquer outro byte desliga a prensa imediatamente.
    Os comandos descritos acima quando recebidos pelo arduino acionam ou desligam os reles. Estes reles estão por sua vez ligados ao inverssor que de acordo 
  com a sequencia binaria recebida pelo acionamento dos reles vai ligar o motor da prensa com uma velocidade e sentido de giro especifico.
    A prensa realiza o ensaio CBR (Indice de Suporte California) de acordo com a norma NBR - 9895 , e o ensaio Marshall de acordo com a norma ME-043/95
*/
int Estado;                              //Variavel de comando do programa
const int forcaPin = A0;                 //Pino onde sera conectado a celula de carga
const int desloPin = A2;                 //Pino onde sera conectado o LVDT
const int rele1Pin = 2;                  //Pino que sera ligado o rele 1
const int rele2Pin = 4;                  //Pino que sera ligado o rele 2
const int ledArduino = 13;               //Led nativo do arduino (sera usado para verificação visual do funcionamento simulando o motor)
unsigned long tempoAtual = 0;            //Tempo atual que sera usado no delay
unsigned long tempoAnterior = 0;         //Tempo de referencia para a nova contagem de tempo
float forca, deslocamento;               //variaveis de carga e deslocamento para receber os valores lidos pelos sensores

void setup() {
  pinMode(forcaPin,INPUT);               //Define que o pino da celula de carga é uma entrada
  pinMode(desloPin,INPUT);               //Define que o pino do LVDT é uma entrada
  pinMode(rele1Pin,OUTPUT);              //Define que o pino do rele 1 é uma saida
  pinMode(rele2Pin,OUTPUT);              //Define que o pino do rele 2 é uma saida
  pinMode(ledArduino,OUTPUT);            //Define que o LED interno do arduino como saida (apenas para teste visual do funcionamento) 
  Serial.begin(256000);                  //Baud da comunicação serial
}

void loop() {

//verifica se a dados sendo recebidos por meio da comunicação serial, caso sim atribui o valor recebido à variavel Estado (variavel de comando) 
  if (Serial.available() > 0) {                      
    Estado = Serial.read();                      
  }

//Liga o motor da prensa em velociade marshall (sentido de giro de compressão)
  if (Estado==251){                                    
    digitalWrite(rele1Pin,LOW);
    digitalWrite(rele2Pin,HIGH);
    digitalWrite(ledArduino,HIGH);
  }
//Liga o motor da prensa em velociade cbr (sentido de giro de compressão)
  else if(Estado==252){                         
    digitalWrite(rele1Pin,HIGH);
    digitalWrite(rele2Pin,LOW);
    digitalWrite(ledArduino,HIGH);
  }
//Liga o motor da prensa em sentido contrario da compressão até que o deslocamento lido seja 0
  else if(Estado==253){
    while (deslocamento > 0.1){             
      digitalWrite(rele1Pin,HIGH);
      digitalWrite(rele2Pin,HIGH);
      digitalWrite(ledArduino,HIGH);
      deslocamento = analogRead(desloPin) * 25.0 / 1023.0;
    }
    Estado = 254;
  }
//Deixa o motor desligado caso nenhum solicitação de ensaio seja enviado ou por solicitação do usuario na pagina de ensaio
  else{                              
    digitalWrite(rele1Pin,LOW);
    digitalWrite(rele2Pin,LOW);
    digitalWrite(ledArduino,LOW);
  }

//A cada periodo de tempo pre definido ele envia por comunicação serial os valores de força e deslocamento
  tempoAtual = millis();    
  if ((tempoAtual - tempoAnterior) > 800){                           //'temporizador' que não 'pausa' o programa
    tempoAnterior = tempoAtual;
    forca = analogRead(forcaPin) * 5000.0 / 1023.0;                  //recebe o valor do sensor e o coverte para a escala real
    deslocamento = analogRead(desloPin) * 25.0 / 1023.0; 
    Serial.println(forca);                                             //Envia o valor de força lido pelo sensor por comunicação serial
    Serial.println(deslocamento);
  }
}

