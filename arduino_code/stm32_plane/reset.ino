void Reset(){
  delay(1000);

  Motor1.attach(PB6,MIN_SIGNAL,MAX_SIGNAL); //a

  Motor1.writeMicroseconds(MAX_SIGNAL);
  delay(7000);
  Motor1.writeMicroseconds(MIN_SIGNAL);
}
