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

  if (Estado==252){ 
    digitalWrite(13,1);                    
    Serial.println('0.0z0.0');          //força
    delay(1000);
    Serial.println('320.0z0.63');
    delay(1000);
    Serial.println('660.0z1.27');
    delay(1000);    
    Serial.println('930.0z1.90');
    delay(1000);  
    Serial.println('1120.0z2.54');
    delay(1000);
    Serial.println('1270.0z3.17');
    delay(1000);
    Serial.println('1420.0z3.81'); 
    delay(1000);
    Serial.println('1620.0z5.80'); 
    delay(1000);
    Serial.println('1790.0z6.35'); 
    delay(1000);
    Serial.println('1990.0z7.32');
    delay(1000);
    Serial.println('2230.0z8.89'); 
    delay(1000);
    Serial.println('2440.0z10.16'); 
    delay(1000);
    Serial.println('2670.0z11.43'); 
    delay(1000);
    Serial.println('2915.0z12.70');    
    delay(1000);
    Serial.println('3535.0z13.58');    
    delay(1000);
  }
  else{
    digitalWrite(13,0);    
    Serial.println('0.0z0.0');
    delay(300);   
    }  
}

