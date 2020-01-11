#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const int REPEAT = 10000;

static const char input[] = "59768092839927758565191298625215106371890118051426250855924764194411528004718709886402903435569627982485301921649240820059827161024631612290005106304724846680415690183371469037418126383450370741078684974598662642956794012825271487329243583117537873565332166744128845006806878717955946534158837370451935919790469815143341599820016469368684893122766857261426799636559525003877090579845725676481276977781270627558901433501565337409716858949203430181103278194428546385063911239478804717744977998841434061688000383456176494210691861957243370245170223862304663932874454624234226361642678259020094801774825694423060700312504286475305674864442250709029812379";

int *input_repeated(int *data_len)
{
    int len = strlen(input);
    int *data = (int *) malloc(sizeof(int) * len * REPEAT);
    if (!data) {
        printf("ooops no memory\n");
        exit(1);
    }
    for (int n = 0; n < REPEAT; n++) {
        for (int i = 0; i < len; i++) {
            data[i + n * len] = input[i] - '0';
        }
    }
    *data_len = len * REPEAT;
    return data;
}

int first_n_digits(int *data, int n)
{
    int result = 0;
    for (int i = 0; i < n; i++) {
        result = result * 10 + data[i];
    }
    return result;
}

void transform_100(int *data, int len)
{
    for (int n = 0; n < 100; n++) {
        for (int i = len - 1; i >= 0; i--) {
            data[i] = (data[i + 1] + data[i]) % 10;
        }
    }
}

void solve2(void)
{
    int data_len = 0;
    int *data = input_repeated(&data_len);
    int offset = first_n_digits(data, 7);

    int *relevant_data = &data[offset];
    int len = data_len - offset;

    transform_100(relevant_data, len);

    int result = first_n_digits(relevant_data, 8);
    printf("Solution 2: %d\n", result);
}

int main(void)
{
    solve2();
    return 0;
}
