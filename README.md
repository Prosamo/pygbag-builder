# pygbag_builder
This is a module to support people who want to make browser game with pygame. Normaly, pygame won't work on web browser but by using pygbag(wasm for pygame), we can publish pygame programs on the internet. 

When we use pygbag, we should pay attention to some points.
 - name the main file as `main.py`
 - call main function with asyncio.run
 - insert await asyncio.sleep(0) into while loops
 - remake some functions into async functions

These points are not fatal probrem if there aren't many while loops. But when we make a little complex games, these points become cumbersome. So, this module aims to support making those game.(This module may not enough to support highly complex game...sorry.)

## Install

```sh
pip install pygbag_builder
```

## How To
### step1
You should make folder for your project at first. The main file must be `main.py` and contain main function. 

These are sample programs. `main.py` can import other `.py`files. The only thing that you should care about is to make main function.

```python:main.py
import pygame, sys
import module
pygame.init()
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption('template')
clock = pygame.time.Clock()

class Class:
    def __init__(self):
        pass
    def loop(self):
        while True:
            break
instance = Class()

def loop():
    while True:
        break


def main():
    color = 0
    while True:
        screen.fill((color, color, color))
        color = min(255, color+1)
        loop()
        instance.loop()
        module.loop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    main()
```

```python:module.py
def loop():
    while True:
        break
```
### step2
please use this command in your project folder
```sh
pygbag_builder main_flow
```

By using this command, your python files are automatically modified like this.
```python:main.py
import asyncio
import pygame, sys
import module
pygame.init()
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption('template')
clock = pygame.time.Clock()


class Class:

    def __init__(self):
        pass

    async def loop(self):
        while True:
            await asyncio.sleep(0)
            break


instance = Class()


async def loop():
    while True:
        await asyncio.sleep(0)
        break


async def main():
    color = 0
    while True:
        await asyncio.sleep(0)
        screen.fill((color, color, color))
        color = min(255, color + 1)
        await loop()
        await instance.loop()
        await module.loop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    asyncio.run(main())
```
```python:module.py
import asyncio


async def loop():
    while True:
        await asyncio.sleep(0)
        break
```

Also, this command creates 'pygbag.yml'(.github/workflows/pygbag.yml)

These files are put in `pygbag_builder_build` folder which created in your project folder.

### step3
Now, you have all the necessary files to upload your game, you can create a repository by following these steps

https://pygame-web.github.io/wiki/publishing/github.io/

#### summary
- run pygbag_build from Action
- set gh-pages to branch from Settings → pages



## License
This project follows MIT. If you need more information, please look at `LICENSE`.

## pygbag
https://pypi.org/project/pygbag/