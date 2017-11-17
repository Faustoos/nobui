#include <SDL.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

void sdl_subsystem(void) {
        if(SDL_Init(SDL_INIT_VIDEO) != 0) {
                fprintf(stderr, "Could not initialize SDL!\n");
                exit(EXIT_FAILURE);
        }
        SDL_Window* win = SDL_CreateWindow(
                "Hello World!",
                100,
                100,
                320,
                240,
                SDL_WINDOW_SHOWN
        );

        if (NULL == win) {
                fprintf(stderr, "Could not create window!\n");
                SDL_Quit();
                exit(EXIT_FAILURE);
        }

        SDL_Renderer* ren = SDL_CreateRenderer(
                win,
                -1,
                SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC
        );

        if (NULL == ren) {
                SDL_DestroyWindow(win);
                fprintf(stderr, "Could not create rendered!\n");
                SDL_Quit();
                exit(EXIT_FAILURE);
        }

        bool quit = false;

        SDL_Event e;
        while(!quit) {
                while(SDL_PollEvent(&e)) {
                        switch(e.type) {
                        case SDL_QUIT:
                                quit = true;
                        }
                }
        }
}
