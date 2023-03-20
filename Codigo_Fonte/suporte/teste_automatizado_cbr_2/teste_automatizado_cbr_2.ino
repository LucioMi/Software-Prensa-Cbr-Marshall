/*
    Este é um codigo para o microcontrolador arduino que visa simular valores de entrada (força e deslocamento) nos pontos criticos que a norma NBR 9895 
  descreve. Os valores são enviados por comunicão serial. 
    A variavel Estado que é recebida por comunicação serial controla o ensaio por meio do byte 252 que indica que o ensaio esta em andamento qualquer outro 
valor indica que o ensaio esta encerrado. 
  */
int Estado;
float deslocamento = 0;
float forca = 0;

void setup() {
  Serial.begin(256000);       //DEFINE INICIO E 'VELOCIDADE' DA COMUNICAÇÃO SERIAL
  pinMode(13,OUTPUT);
}

void loop() {
  
  if (Serial.available() > 0) {                  //verifica se a dados sendo recebidos por meio da comunicação serial       
    Estado = Serial.read();                     // se estiver recebendo os dados os atribui à variavel Estado
  }

  if (Estado==252){ 
    deslocamento = deslocamento + 0.01;
    forca = forca + 2.0;
    Serial.println(forca);
    Serial.println(deslocamento); 
    delay(100);
  }
  else{
    digitalWrite(13,0);    
    Serial.println(0.0);
    Serial.println(0.0);  
    delay(300);   
    }  
}

