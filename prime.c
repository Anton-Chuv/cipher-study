int isPrime(unsigned long long n){
    char false = 0;
    char true = 1;
    if (n < 2) return false;
    if (n == 2) return true;
    if (n == 3) return true;
    if (n % 2 == 0) return false;
    if (n % 3 == 0) return false;

    unsigned long long i = 5;
    int w = 2;

    while (i*i <= n){
        if (n % i == 0) return false;

        i += w;
        w = 6 - w;
    }

    return true;
}

unsigned long long getPrime(unsigned long long n){
    while (!(isPrime(--n)));
    return n;
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


// gcc -fPIC -shared -o libprime.so prime.c