/******* FileLib_osx   ************************ 2015.2.12 *****************
  This program is included any program for file input and output.
  (This function return the length that read data from the file.)

  AnyFileRead(file,data,len)  : Any style data to Double
  AnyFileWrite(file,data,len) : Any style data to Double
  
  char    file;
  double  *data;
  unsigned long  length;
  
  file:
  To read  the filename, this style must be character ( char ). and necessary
  the subscribe, '.dxx' or '.DXX' means data style, the style was decided
  by Shimada.
  
  data:
  To store the address of data. It was declared Double before.
  
  len:
  length of data. it is integer.

*****************************************************************************/
/******* Filelib_shimada ************************ 1996.2.15 *****************
  This program is included any program for file input and ooutput.
  (This function return the length that read data from the file.)

  AnyFileRead(file,data,len)  : Any style data to Double
  AnyFileWrite(file,data,len) : Any style data to Double
  
  char    file;
  double  *data;
  unsigned long  length;
  
  file:
  To read  the filename, this style must be character ( char ). and necessary
  the subscribe, '.dxx' means data style, the style was decided by Shimada.
  
  data:
  To store the addres of data. It was declared Double before.
  
  len:
  lehgth of data. it is integer.

*****************************************************************************/
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

int AnyFile_error(int n)
{
    switch(n)
    {
        case 1:	printf("File Open Error !!\n");	return(-1);
        case 2:	printf("Bad data style !!\n");	return(-1);
    }
    return 0;
}


int style(char *name)
{
    int i,j,k;
    //    static char *ds[14]={".dsa",".dfa",".dda",".dsb",".dfb",".ddb",".xy",
    //                        ".DSA",".DFA",".DDA",".DSB",".DFB",".DDB",".XY"};
    static char *ds[6]={".DSA",".DFA",".DDA",".DSB",".DFB",".DDB"};
    
    for(k=0;k<6;k++)
    {
        j=0;
        for(i=0;i<(int)strlen(ds[k]);i++)
        {
            if(name[(int)strlen(name)-(int)strlen(ds[k])+i] == ds[k][i])
                j++;
            
            if( j == (int)strlen(ds[k]))
                return(k+1);
        }
    }
    AnyFile_error(2);
    return 0;
}

int lenfile(char *name)
{
    FILE *fp;
    unsigned long i,j,k;
    double data,data2;
    short  datas;
    static char da[4][10]={"%d","%e","%le","%le %le"};
    static int  db[3]={2,4,8};
    
    i=style(name)-1;
    j=0;
    
    if( i < 3 )
    {
        if( (fp=fopen(name,"r")) == NULL ) 	    AnyFile_error(1);
        while( fscanf(fp,da[i],&data) == 1 ) j++ ;
        fclose(fp);
        return(j);
    }
    else
    {
        if( (fp=fopen(name,"rb")) == NULL )	    AnyFile_error(1);
        while( fread(&data,db[i-3],1,fp) == 1 ) j++ ;
        fclose(fp);
        return(j);
    }
}





int read_DSAfile(char *name,double *data,int len)
{
    int n,data_int;
    FILE *fin;
    if((fin=fopen(name,"r")) == NULL )
    	AnyFile_error(1);
    n=0;
    while( fscanf(fin,"%d",&data_int) == 1 && n < len )
    	data[n++]=(double)data_int;     
    fclose(fin);
    return(n);
}
    
int read_DFAfile(char *name,double *data,int len)
{
    FILE *fin;
    int n;
    float data_float;
    if((fin=fopen(name,"r")) == NULL  )
	AnyFile_error(1);
    n=0;
    while( fscanf(fin,"%e",&data_float) == 1 && n < len )
	data[n++]=(double)data_float;
    fclose(fin);
    return(n);
}
    
int read_DDAfile(char *name,double *data,int len)
{
    FILE *fin;
    int n;
    double data_double;
    if((fin=fopen(name,"r")) == NULL )
    	AnyFile_error(1);
    n=0;
    while( fscanf(fin,"%le",&data_double) == 1  && n < len )
    	data[n++]=(double)data_double;
    fclose(fin);    
    return(n);
}
    
int read_DSBfile(char *name,double *data,int len)
{
    FILE *fin;
    int n,i,size;    
    short data_int;                                           
    char *data_char,tmp;
    if((fin=fopen(name,"rb")) == NULL )
        AnyFile_error(1);
    n=0;                                                      
    while((fread(&data_int,sizeof(short),1,fin)) == 1 && n < len ){
        data[n++]=(double) data_int;
    }
    fclose(fin);
    return(n);                                    
}
    
int read_DFBfile(char *name,double *data,int len)
{
    FILE *fin;
    int n,i,size;
    float data_float;
    char *data_char,tmp;
    if((fin=fopen(name,"rb")) == NULL )
        AnyFile_error(1);
    n=0;                                                      
    while((fread(&data_float,sizeof(float),1,fin)) == 1 && n < len ){
        data[n++]=(double) data_float;
    }
    fclose(fin);
    return(n);
}                                                             

int read_DDBfile(char *name,double *data,int len)
{
    FILE *fin;
    int m,n,i,size;                                                  
    double data_double;                                           
    char *data_char,tmp;
    if((fin=fopen(name,"rb")) == NULL )        AnyFile_error(1);
    n=0;                                                      
    while((fread(&data_double,sizeof(double),1,fin)) == 1 && n-1 < len ){
        data[n++]= data_double;
    }
    fclose(fin);
    return(n);                                                
}

int AnyFileRead(char *name,double *data,int len)
{
    //    int m,n;
    /*
     switch(style(name))
     {
     case -1:	AnyFile_error(2);	return(-1);
     case 1:	read1(name,data,len);	break;
     case 2:	read2(name,data,len);	break;
     case 3:	read3(name,data,len);	break;
     case 4:	read4(name,data,len);	break;
     case 5:	read5(name,data,len);	break;
     case 6:	read6(name,data,len);	break;
     case 7:	read7(name,data,len);   break;
     case 8:	read1(name,data,len);   break;
     case 9:	read2(name,data,len);   break;
     case 10:	read3(name,data,len);   break;
     case 11:	read11(name,data,len);  break;
     case 12:	read12(name,data,len);  break;
     case 13:	read13(name,data,len);  break;
     case 14:	read7(name,data,len);   break;
     }*/
    
    switch(style(name))
    {
        case -1:	AnyFile_error(2);	return(-1);
        case  1:	read_DSAfile(name,data,len);	break;
        case  2:	read_DFAfile(name,data,len);	break;
        case  3:	read_DDAfile(name,data,len);	break;
        case  4:	read_DSBfile(name,data,len);	break;
        case  5:	read_DFBfile(name,data,len);	break;
        case  6:	read_DDBfile(name,data,len);	break;
    }
    return 0;
}


/******* Filelib_shimada ******************************************************
  This program is included any program for file input and ooutput.
  (This function return the length that read data from the file.)

  AnyFileWrite(file,data,len) : Any style data to Double
  
  char    file;
  double  *data;
  int     length;
  
  file:
  To read  the filename, this style must be character ( char ). and necessary
  the subscribe, '.dxx' means data style, the style was decided by Shimada.
  
  data:
  To store the addres of data. It was declared Double before.
  
  len:
  lehgth of data. it is integer.

*****************************************************************************/


int write_DSAfile(char *name,double *data,int len)
{
    int n;
    short data_short;
    FILE *fout;
    
    if((fout=fopen(name,"w")) == NULL )	AnyFile_error(1);
    n=0;
    while( n < len ){
        data_short=(short)(data[n++]);
        fprintf(fout,"%d\n",data_short);
    }
    fflush(fout);
    fclose(fout);
    return(n);
}
    
int write_DFAfile(char *name,double *data,int len)
{
    FILE *fout;
    int n;
    float data_float;
  
    if((fout=fopen(name,"w")) == NULL  )	AnyFile_error(1);
    n=0;
    while( n < len ){
    	data_float=(float)data[n++];
	    fprintf(fout,"%e\n",data_float);
    }
    fflush(fout);
    fclose(fout);
    return(n);
}
    
int write_DDAfile(char *name,double *data,int len)
{
    FILE *fout;
    int n;

    if((fout=fopen(name,"w")) == NULL )	AnyFile_error(1);
    n=0;
    while( n < len)
    {
        fprintf(fout,"%le\n",data[n]);
        n++;
    }
    fflush(fout);
    fclose(fout);    
    return(n);
}

int write_DSBfile(char *name,double *data,int len)
{
    FILE *fout;
    int n,i,j,size;    
    short *data_int;
    char *data_char,tmp;

    data_int=(short *)malloc(sizeof(short)*len);
    if((fout=fopen(name,"wb")) == NULL ) AnyFile_error(1);

    for(n=0;n<len;n++) data_int[n]=(short)data[n];
    n=fwrite(data_int,sizeof(short),len,fout);
    fflush(fout);
    fclose(fout);
    return(n);                                    
}                                                             

int write_DFBfile(char *name,double *data,int len)
{
    FILE *fout;
    int n,i,j,size;
    float *data_float;
    char *data_char,tmp;

    data_float=(float *)malloc(sizeof(float)*len);
    if((fout=fopen(name,"wb")) == NULL ) AnyFile_error(1);

    for(n=0;n<len;n++) data_float[n]=(float)data[n];
    n=fwrite(data_float,sizeof(float),len,fout);
    fflush(fout);
    fclose(fout);
    return(n);                                                
}       

int write_DDBfile(char *name,double *data,int len)
{
    FILE *fout;
    int n,i,j,size;                    
    char *data_char,tmp;
    double *data_double;

    data_double=(double *)malloc(sizeof(double)*len);
    if((fout=fopen(name,"wb")) == NULL )       AnyFile_error(1);

    for(n=0;n<len;n++) data_double[n]=data[n];
    n=fwrite(data_double,sizeof(double),len,fout);
    fflush(fout);
    fclose(fout);
    return(n);                                                
}                                                             

int AnyFileWrite(char *name,double *data,int len)
{
    //int m,n;
    /*
     switch(style(name)){
     case  -1:	AnyFile_error(2);	return(-1);
     case   1:   write1(name,data,len);	break;//DSA file
     case   2:	write2(name,data,len);	break;//DFA file
     case   3:	write3(name,data,len);	break;//DDA file
     case 1+3:	write4(name,data,len);	break;//DSB file
     case 2+3:	write5(name,data,len);	break;//DFB file
     case 3+3:	write6(name,data,len);	break;//DDB file
     case   7:	write7(name,data,len);  break;
     case   8:	write1(name,data,len);  break;
     case   9:	write2(name,data,len);  break;
     case  10:	write3(name,data,len);  break;
     case  11:	write11(name,data,len); break;
     case  12:	write12(name,data,len); break;
     case  13:	write13(name,data,len); break;
     case  14:	write7(name,data,len);  break;
     }*/
    
    switch(style(name)){
        case  -1:	AnyFile_error(2);	return(-1);
        case   1:  write_DSAfile(name,data,len);	break;
        case   2:	write_DFAfile(name,data,len);	break;
        case   3:	write_DDAfile(name,data,len);	break;
        case   4:	write_DSBfile(name,data,len);	break;
        case   5:	write_DFBfile(name,data,len);	break;
        case   6:	write_DDBfile(name,data,len);	break;
    }
    
    return(1);
}

