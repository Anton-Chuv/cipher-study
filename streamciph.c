#include <stdlib.h>
//#include <stdio.h>

#define int128 __int128

void lfsrGen(int128 lfsr[3], char key[30]) {
    key[0]  &= 0x7f; // не правильно так делать
    key[10] &= 0x7f;
    key[20] &= 0x7f;
    for (size_t i = 0; i < 3; i++)
        for (size_t j = 0; j < 10; j++) {
            lfsr[i]<<=8;
            lfsr[i] += key[i*10 + j];
        }
}

char getFeedbackBit(int128 lfsr, int bits_pos[4]) {
    char result = 0;
    for (size_t i = 0; i < 4; i++)
        result ^= (lfsr>>bits_pos[i]) & 1; 
    return result;
}

char genGammaByte(int128 lfsr[3]) {
    char result = 0xff;
    int bitsBackConnection[3][4] = {
            {75, 6, 3, 1},
            {76, 6, 5, 2},
            {78, 4, 3, 2}
        };
    for (size_t i = 0; i < 8; i++) {
        result<<=1;
        result |= (lfsr[1] & 1) ^ (lfsr[2] & 1);
        if (!(lfsr[0] & 1<<2)){
            lfsr[1] |= ((int128)getFeedbackBit(lfsr[1], bitsBackConnection[1]))<<77;
            lfsr[1]>>=1;
        }
        if (!(lfsr[0] & ((int128)1)<<77)) {
            lfsr[2] |= ((int128)getFeedbackBit(lfsr[2], bitsBackConnection[2]))<<79;
            lfsr[2]>>=1;
        }
        lfsr[0] |= ((int128)getFeedbackBit(lfsr[0], bitsBackConnection[0]))<<77;
        lfsr[1] |= ((int128)getFeedbackBit(lfsr[1], bitsBackConnection[1]))<<77;
        lfsr[2] |= ((int128)getFeedbackBit(lfsr[2], bitsBackConnection[2]))<<79;
        for (size_t j = 0; j < 3; j++)
            lfsr[j]>>=1;
        //count1 += getFeedbackBit(lfsr[1], bitsBackConnection[1]);
        //count++;
    }
    return result;
} 

char* ciph(char* input, char* key, long long int input_bytelen) {
    int128 lfsr[3]= {0, 0, 0};
    char gamma = 0;
    lfsrGen(lfsr, key);
    for (int i = 0; i < input_bytelen; i++) {
        gamma = genGammaByte(lfsr);    
        input[i] ^= gamma;
    }
    return input;
}

/*
int main(int argc, char const *argv[]) {
    
    char key[30];
    for (int i = 0; i < 30; i++)
        key[i] = 0xaa+i;

    int bytelen = 10; // один блок 8 байт
    int128 lfsr[3];
    lfsr[0] = 0x123456789abcde; // хоть и подчеркивает но записывает тройку коректно, но криво выводится в консоль
    //lfsr[0] = (int128)0x123456789abcdef1200; // хоть и подчеркивает но записывает тройку коректно, но криво выводится в консоль
    lfsr[1] = lfsr[0] + 1;
    lfsr[2] = lfsr[0] + 2;
    char* input_mod = (char*)malloc((bytelen) * sizeof(char));
    for (size_t i = 0; i < bytelen; i++) 
        input_mod[i] = i * i;
    for (size_t i = 0; i < bytelen; i++) 
        printf("%02hhx ", input_mod[i]);
    printf("\n");


    
    ciph(input_mod, key, bytelen);
    printf("\n");
    for (size_t i = 0; i < bytelen; i++) 
        printf("%02hhx ", input_mod[i]);
    printf("\n");
    ciph(input_mod, key, bytelen);
    printf("\n");
    for (size_t i = 0; i < bytelen; i++) 
        printf("%02hhx ", input_mod[i]);
    printf("\n");
    return 0;
}
*/

// cc -xc -fPIC -shared -o libstreamciph.so streamciph.c

// для работы int128 добавь флаги -xc в tasks.json