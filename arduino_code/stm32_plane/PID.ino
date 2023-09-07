#define Rate_I_MAX 100

void Function_PID(float *err, PID *val, int r, int c, double dt){

  val->P = PID_Val[r][c] * (*err);
  val->I += PID_Val[r][c+1] * (val->err_last + (*err)) * dt/2;
  if(val->I > Rate_I_MAX) {
    val->I = Rate_I_MAX;
  }
  else if(val->I < -Rate_I_MAX){
    val->I = -Rate_I_MAX;
  }
  val->D = ((*err) - val->err_last ) * PID_Val[r][c+2];
  val->err_last = (*err);
  
}
