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

void loop() {
  
  if (Serial.available() > 0) {                  //verifica se a dados sendo recebidos por meio da comunicação serial       
    Estado = Serial.read();                     // se estiver recebendo os dados os atribui à variavel Estado
  }

  if (Estado==251){ 
    digitalWrite(13,1);                    
    Serial.println("0.0z0.0");
    delay(800);
    Serial.println("660.0z1.27");
    delay(800);    
    Serial.println("1120.0z2.54"); 
    delay(800);
    Serial.println("1420z3.81"); 
    delay(800);
    Serial.println("1620.37z5.80"); 
    delay(800);
    Serial.println("1790.890z6.35");
    delay(800);
    Serial.println("3000.52z8.89");
    delay(800);
    Serial.println("2800.21z10.43");
    delay(800);
    Serial.println("2194.67z12.05");
    delay(800);
    Serial.println("2000.35z14.37");  
    delay(800);
    Serial.println("1910.0z14.50");
    delay(800);
    Serial.println("1800.09z15.02");    
    delay(800);
  }
  else{
    digitalWrite(13,0);    
    Serial.println("0.0z0.0");
    delay(300);   
    }  
}