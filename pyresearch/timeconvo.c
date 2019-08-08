#include <stdio.h>
#include <stdlib.h>
#include "FileLib_osx.c"


void help(void)
{
  fprintf(stderr,"> \t Linear convolution  Ver.2.0  by Y.Shimazu ");
  fprintf(stderr,"2001-07-10\n");
  fprintf(stderr,"> Usage: convo [infile1] [infile2] [outfile] \n");
  fprintf(stderr,">\n");
  exit(EXIT_FAILURE);
}


int main(int argc, char **argv){

  int    n,p,i;
  int    N1,N2;
  double  *x, *h, *y;
  
  if(argc != 4){
    help();
    exit(EXIT_FAILURE);
  }
  
  N1 = lenfile(argv[1]);
  N2 = lenfile(argv[2]);
  
  x = (double *)calloc(N1, (size_t)sizeof(double));
  h = (double *)calloc(N2, (size_t)sizeof(double));
  y = (double *)calloc(N1+N2, (size_t)sizeof(double));
  
  fprintf(stderr,"> calculate convolution...\n");
  fprintf(stderr,"> signal length  %d / %d\n",N1,N2);

  /*input data x[n], h[n]*/
  fprintf(stderr,"> input : file1, file2 > ...");
  AnyFileRead(argv[1],x,N1);
  AnyFileRead(argv[2],h,N2);
  fprintf(stderr," OK. \n");
  
  
  /* calculating convolution 69 */    
  for(p=0;p<N1;p++){
    fprintf(stderr,"%2d [%%]",(int)((double)p/(double)N1*100.0+0.5));
    for (n=p;n<N2+p;n++){
      y[n] += x[p] * h[n-p];
    }    
    fprintf(stderr,"\b\b\b\b\b\b");
  }
  
  
  /*output data y[n]*/
  AnyFileWrite(argv[3],y,N1+N2);
  fprintf(stderr,"> Completed.\n");
  
}

