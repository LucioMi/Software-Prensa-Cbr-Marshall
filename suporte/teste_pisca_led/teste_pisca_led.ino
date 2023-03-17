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
  }
  else if (Estado==254){
    digitalWrite(13,0);    
    Serial.println(0.00);          //força
    Serial.println(0.00);          //deslocamento
  }else if (Estado==253){
    digitalWrite(13,0);    
    delay(300);
    digitalWrite(13,1);
    Serial.println(0.00);          //força
    Serial.println(0.00);          //deslocamento 
  }
  
  delay(300);


  
}

