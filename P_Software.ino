//ESTE PROGRAMA POR ENQUANTO SO SELECIONA O MODO DE FUNCIONAMENTO PELAS INFORMAÇOES RECEBIDAS POR COMUNICAÇÃO SERIAL E ENVIA OS VALORES RECEBIDOS
//PELOS SENSORES POR COMUNICAÇÃO SERIAL. AINDA NÃO FOI CRIADO UMA FUNÇÃO PARA PARAR A PRENSA NEM AQUI E NEM NO PYTHON
const int ForPin = A0;              //pino da celula de carga
const int DesPin = A2;              //pino do sensor de deslocamento
const int R1Pin = 2;               //pino do rele de comando
const int R2Pin = 4;               //pino do rele de comando
float forca, deslocamento;         //variaveis que guardaram força e deslocamento
int Estado;                         //define estado 251=Marshall, 252=Cbr, 253=Parada, 254=Retona à posição 0 do sensor de deslocamento

void setup() {
  // declara sensores como entrada reles como saida e inicia a comunicação serial
  pinMode(ForPin, INPUT);  
  pinMode(DesPin, INPUT);
  pinMode(R1Pin, OUTPUT);
  pinMode(R2Pin, OUTPUT);
  pinMode(13, OUTPUT);
  Serial.begin(256000);
}

void loop() {
//verifica se a dados sendo recebidos por meio da comunicação serial
  if (Serial.available() > 0) {                 
    Estado = Serial.read();                     // se estiver recebendo os dados ele guarda este valor na variavel Estado
  }


  if (Estado==251){            //Liga o rele 1 que faz a prensa funcionar em modo marshall (deve-se configurar essa funcionalidade no inversor de frequencia)
    digitalWrite(R1Pin, HIGH);              
  }
  else if (Estado==252){          //Liga o rele 2 que faz a prensa funcionar em modo CBR (deve-se configurar essa funcionalidade no inversor de frequencia)            
    digitalWrite(R2Pin, HIGH);         
  }
  else if (Estado==253){          //Liga o rele 1 e o rele 2 que faz a prensa retornar (deve-se configurar essa funcionalidade no inversor de frequencia)
    digitalWrite(R1Pin, HIGH);
    digitalWrite(R2Pin, HIGH);
  }
  else {
    digitalWrite(R1Pin, LOW);     //Desliga a prensa caso um valor diferente dos acima seja recebido
    digitalWrite(R2Pin, LOW);
  }

//Envia os valores de força e deslocamento recebido pelos sensores por meio de comunicação serial (valores convertidos para ser compativel com o software)
  forca = map(analogRead(ForPin), 0, 1023, 0, 500000);
  deslocamento = map(analogRead(DesPin), 0, 1023, 0, 2500);
  Serial.println(forca);
  Serial.println(deslocamento);
  delay(300);
}