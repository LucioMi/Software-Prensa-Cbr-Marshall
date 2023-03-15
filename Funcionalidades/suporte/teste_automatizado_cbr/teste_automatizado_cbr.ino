/*
    Este é um codigo para o microcontrolador arduino que visa simular valores de entrada (força e deslocamento) nos pontos criticos que a norma NBR 9895 
  descreve. Os valores são enviados por comunicão serial. 
    A variavel Estado que é recebida por comunicação serial controla o ensaio por meio do byte 252 que indica que o ensaio esta em andamento qualquer outro 
valor indica que o ensaio esta encerrado. 
  */
int Estado;

void setup() {
  Serial.begin(256000);       //DEFINE INICIO E 'VELOCIDADE' DA COMUNICAÇÃO SERIAL
  pinMode(13,OUTPUT);
}
//(130987.00
//659.00)
void loop() {
  
  if (Serial.available() > 0) {                  //verifica se a dados sendo recebidos por meio da comunicação serial       
    Estado = Serial.read();                     // se estiver recebendo os dados os atribui à variavel Estado
  }

  if (Estado==251){ 
    digitalWrite(13,1);                    
    Serial.println(0.00);          //força
    Serial.println(0.00);          //deslocamento
    delay(1000);
    Serial.println(32000.00);
    Serial.println(63.00);
    delay(1000);
    Serial.println(66000.00);
    Serial.println(127.00); 
    delay(1000);    
    Serial.println(93000.00);
    Serial.println(190.00); 
    delay(1000);  
    Serial.println(112000.00);
    Serial.println(254.00); 
    delay(1000);
    Serial.println(127000.00);
    Serial.println(317.00); 
    delay(1000);
    Serial.println(142000.00);
    Serial.println(381.00); 
    delay(1000);
    Serial.println(162000.00);
    Serial.println(580.00); 
    delay(1000);
    Serial.println(179000.00);
    Serial.println(635.00); 
    delay(1000);
    Serial.println(223000.00);
    Serial.println(889.00); 
    delay(1000);
    Serial.println(267000.00);
    Serial.println(1143.00); 
    delay(1000);
    Serial.println(291000.00);
    Serial.println(1270.00); 
    delay(1000);
    Serial.println(303500.00);
    Serial.println(1347.00);    
    delay(1000);
    Serial.println(313500.00);
    Serial.println(1401.00);    
    delay(1000);
  }
  else{
    digitalWrite(13,0);    
    Serial.println(0.00);
    Serial.println(0.00);  
    delay(300);   
    }  
}

