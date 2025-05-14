#include <stdlib.h>

void subkeysGen(unsigned short int* key, unsigned short int subkeys[][6]) {
    unsigned short int key_mod[10];
    for (int i = 0; i < 10; i++)
        key_mod[i] = key[i];
    key_mod[8] = key_mod[0];
    key_mod[9] = key_mod[1];
    for (int i = 0; i < 7; i++) {
        for (int j = 0; j < 8; j++)
            subkeys[(i * 8 + j) / 6][(i * 8 + j) % 6] = key_mod[j];
        // побитовый сдвиг влево на 25 (16 + 9)
        for (int j = 0; j < 8; j++)
            key_mod[j] = key_mod[j + 1] << 9 | key_mod[j + 2] >> (16 - 9);
        key_mod[8] = key_mod[0];
        key_mod[9] = key_mod[1];
    }
}

unsigned short int mulMod(unsigned short int a, unsigned short int b) {
    if (a == 0 && b == 0)
        return 1;
    if (a == 0)
        return ((unsigned int)(65536 * b) % 65537 == 65536) ? 0: (unsigned int)(65536 * b) % 65537;
    if (b == 0)
        return ((unsigned int)(65536 * a) % 65537 == 65536) ? 0: (unsigned int)(65536 * a) % 65537;
    return ((unsigned int)(a * b) % 65537 == 65536) ? 0: (unsigned int)(a * b) % 65537;
}

void blockCiph(unsigned short int block[4], unsigned short int subkeys[][6]) {
    unsigned short int A, B, C, D, E, F;
    for (int i = 0; i < 8; i++) {
        A = mulMod(block[0], subkeys[i][0]);
        B = block[1] + subkeys[i][1];
        C = block[2] + subkeys[i][2];
        D = mulMod(block[3], subkeys[i][3]);
        E = A ^ C;
        F = B ^ D;
        block[0] = A ^ mulMod(F + mulMod(E, subkeys[i][4]), subkeys[i][5]);
        block[1] = C ^ mulMod(F + mulMod(E, subkeys[i][4]), subkeys[i][5]);
        block[2] = B ^ (mulMod(E, subkeys[i][4]) + mulMod((F + mulMod(E, subkeys[i][4])), subkeys[i][5]));
        block[3] = D ^ (mulMod(E, subkeys[i][4]) + mulMod((F + mulMod(E, subkeys[i][4])), subkeys[i][5]));
    }
    block[0] = mulMod(block[0], subkeys[8][0]);
    unsigned short int tmp = block[1];
    block[1] = block[2] + subkeys[8][1];
    block[2] = tmp + subkeys[8][2];
    block[3] = mulMod(block[3], subkeys[8][3]);
}

unsigned short int divMod(unsigned short int a) {
    int M = 0x10001;
    int A = a;
    // This function is Euclidean Algorithm
    int m0 = M;
    int y = 0, x = 1;
 
    while (A > 1) {
        // q is quotient
        int q = A / M;
        int t = M;
 
        // m is remainder now, process same as
        // Euclid's algo
        M = A % M;
        A = t;
        t = y;
 
        // Update y and x
        y = x - q * y;
        x = t;
    }
 
    // Make x positive
    if (x < 0)
        x += m0;
 
    return x;
}

unsigned short int* ciph(unsigned short int* input, unsigned short int* key, long long int input_bytelen) {
    unsigned short int subkeys[9][6];
    subkeysGen(key, subkeys);
    // unsigned short int* input_mod = (unsigned short int*)malloc((input_bytelen / 2 + 1) * sizeof(unsigned short int));
    blockCiph(&input[0], subkeys);
    for (int i = 4; i < input_bytelen / 2; i += 4) {
        for (int j = 0; j < 4; j++)
            input[i + j] ^= input[i - 4 + j];
        blockCiph(&input[i], subkeys);
    }
    return input;
}

unsigned short int* deciph(unsigned short int* input, unsigned short int* key, long long int input_bytelen) {
    unsigned short int subkeys[9][6];
    subkeysGen(key, subkeys);
    unsigned short int subkeys_rev[9][6];
    for (size_t i = 0; i < 8; i++) {
        subkeys_rev[i][0] = divMod(subkeys[8-i][0]);
        subkeys_rev[i][1] = 0x10000 - subkeys[8-i][2];
        subkeys_rev[i][2] = 0x10000 - subkeys[8-i][1];
        subkeys_rev[i][3] = divMod(subkeys[8-i][3]);
        subkeys_rev[i][4] = subkeys[(7-i)][4];
        subkeys_rev[i][5] = subkeys[(7-i)][5];      
    }
    {
        subkeys_rev[0][1] = 0x10000 - subkeys[8][1];
        subkeys_rev[0][2] = 0x10000 - subkeys[8][2];
        subkeys_rev[8][0] = divMod(subkeys[0][0]);
        subkeys_rev[8][1] = 0x10000 - subkeys[0][1];
        subkeys_rev[8][2] = 0x10000 - subkeys[0][2];
        subkeys_rev[8][3] = divMod(subkeys[0][3]);
    }
    

    for (int i = input_bytelen / 2; i > 0; i -= 4) {
        blockCiph(&input[i], subkeys_rev);
        for (int j = 0; j < 4; j++)
            input[i + j] ^= input[i - 4 + j];
    }
    blockCiph(&input[0], subkeys_rev);
    return input;
}

/*
int main(int argc, char const *argv[]) {
    
    unsigned short int key[8];
    for (int i = 0; i < 8; i++)
        key[i] = i + 1;

    int bytelen = 8 * 10; // один блок 8 байт

    unsigned short int* input_mod = (unsigned short int*)malloc((bytelen / 2) * sizeof(unsigned short int));
    for (size_t i = 0; i < (bytelen / 2); i++) 
        input_mod[i] = i;

    ciph(input_mod, key, bytelen);

    deciph(input_mod, key, bytelen);
    
    // printf("%04x ", 0x9d42 * 0xe001);
    // printf("%04x ", 0x899a5d42 % 0x10001);
    // printf("%04x ", 0x9d42 * 0xe001 % 0x10001); // ПОЧЕМУ ЭТО СЧИТАЕТСЯ не правильно 

    return 0;
}
*/

// cc -fPIC -shared -o libidea.so idea.c