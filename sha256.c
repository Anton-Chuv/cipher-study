#include <stdlib.h>
#define rotr(x, k) ((x>>k)|(x<<(32-k)))

unsigned int* sha256(char* input, long long int input_bytelen, unsigned hash[8]) {
    //long int len = (input_bytelen-1) / 4 + 1; // message length in 32 bit

    // начальные значения, квадратные корни простых чисел (взял из википедии)
    hash[0] = 0x6a09e667;
    hash[1] = 0xbb67ae85;
    hash[2] = 0x3c6ef372;
    hash[3] = 0xa54ff53a;
    hash[4] = 0x510e527f;
    hash[5] = 0x9b05688c;
    hash[6] = 0x1f83d9ab;
    hash[7] = 0x5be0cd19;
    unsigned k[64] = {
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    };
    // дополнение входного сообщения
    int addition = 64 - (input_bytelen % 64);
    if (addition<3)
        addition += 64;
    
    //unsigned m[(input_bytelen+addition)/4];
    unsigned* m = malloc((input_bytelen+addition)/4*sizeof(unsigned));
    for (size_t i = 0; i < (input_bytelen+addition)/4 ; i++)
        m[i] = 0;
    for (size_t i = 0; i < input_bytelen; i++)
        m[i/4] += input[i]<<(8*(3-(i%4)));
    m[input_bytelen/4] += 0x80<<(8*(3-(input_bytelen%4)));
    long int len = (input_bytelen+addition)/4;
    m[len-1] = input_bytelen * 8;
    m[len-2] = (input_bytelen * 8)>>32;
    //unsigned word[64];
    unsigned* word = malloc(64*sizeof(unsigned));
    for (int i = 0; i < len; i += 16) { // 16 words = 1 block
        // Extend the first 16 words into the remaining 48 words w[16..63] of the message schedule array:
        for (size_t j = 0; j < 16; j++)
            word[j] = m[i+j];
        for (size_t j = 16; j < 64; j++) {
            word[j] = (rotr(word[j-15], 7) ^ rotr(word[j-15], 18) ^ (word[j-15]>>3));
            word[j] += word[j-16] + word[j-7];
            word[j] += (rotr(word[j-2], 17) ^ rotr(word[j-2], 19)  ^ (word[j-2]>>10));
        }
        unsigned a = hash[0], b = hash[1], c = hash[2], d = hash[3], e = hash[4], f = hash[5], g = hash[6], h = hash[7];
        for (size_t j = 0; j < 64; j++) { 
            unsigned temp1 = k[j] + word[j];
            temp1 += h;
            temp1 += (rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25));
            temp1 += ((e & f)^((~e) & g));
            unsigned temp2 = (rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22));
            temp2 += ((a & b)^(a & c)^(b & c));
            h = g;
            g = f;
            f = e;
            e = d + temp1;
            d = c;
            c = b;
            b = a;
            a = temp1 + temp2;
        }
        hash[0] = hash[0] + a % 0x100000000;
        hash[1] = hash[1] + b % 0x100000000;
        hash[2] = hash[2] + c % 0x100000000;
        hash[3] = hash[3] + d % 0x100000000;
        hash[4] = hash[4] + e % 0x100000000;
        hash[5] = hash[5] + f % 0x100000000;
        hash[6] = hash[6] + g % 0x100000000;
        hash[7] = hash[7] + h % 0x100000000;
    }
    return hash;
}
/*
int main(int argc, char const *argv[]) {
    unsigned hash[8];
    char* input = "abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu";
    int bytelen = strlen(input);
    sha256(input, bytelen, hash);
    for (size_t i = 0; i < 8; i++)
        printf("%08x ", hash[i]);
    

    return 0;
}
*/


// cc -fPIC -shared -o libidea.so idea.c