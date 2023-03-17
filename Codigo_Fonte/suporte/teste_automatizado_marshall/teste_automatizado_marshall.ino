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
    Serial.println(0.0);          //força
    Serial.println(0.0);          //deslocamento
    delay(800);
    Serial.println(660.0);
    Serial.println(1.27); 
    delay(800);    
    Serial.println(1120.0);
    Serial.println(2.54); 
    delay(800);
    Serial.println(1420.0);
    Serial.println(3.81); 
    delay(800);
    Serial.println(1620.0);
    Serial.println(5.80); 
    delay(800);
    Serial.println(1790.0);
    Serial.println(6.35); 
    delay(800);
    Serial.println(3000.0);
    Serial.println(8.89); 
    delay(800);
    Serial.println(2800.0);
    Serial.println(10.43); 
    delay(800);
    Serial.println(2194.60);
    Serial.println(12.05); 
    delay(800);
    Serial.println(2000.0);
    Serial.println(14.0);    
    delay(800);
    Serial.println(1900.0);
    Serial.println(14.50);    
    delay(800);
    Serial.println(1800.0);
    Serial.println(14.90);    
    delay(800);

  }
  else{
    digitalWrite(13,0);    
    Serial.println(0.0);
    Serial.println(0.0);  
    delay(300);   
    }  
}