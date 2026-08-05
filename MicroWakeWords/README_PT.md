# Wake Word em Português (microWakeWord v2)

## Estado atual
Não existe um modelo **microWakeWord v2** público e pronto a usar para português europeu.
Os modelos incluídos (okay_nabu, hey_jarvis, alexa, hey_mycroft) funcionam bem como ativação
genérica, mas não são em português.

## Opções

### 1. Usar um dos modelos incluídos (recomendado para já)
Os modelos por omissão já vêm configurados no YAML. Ativa/desativa no dispositivo via Home Assistant
(entidade de wake word no dispositivo).

### 2. Treinar o teu próprio wake word (requer conta, ~1h)
O [microWakeWord](https://microwakeword.com/) permite treinar um modelo em **português** de graça:

1. Acede a https://microwakeword.com/ e cria conta.
2. Escolhe a frase (ex.: "Olá Xiaozhi", "OK Robô").
3. Seleciona "Portuguese" como idioma de treino.
4. Descarrega os ficheiros `.json` + `.tflite` gerados.

### 3. Usar os teus ficheiros treinados no YAML
Coloca os ficheiros no teu repositório (ex.: `MicroWakeWords/models/v2/`) e adiciona ao YAML:

```yaml
micro_wake_word:
  id: mww
  models:
    - model: https://raw.githubusercontent.com/ricardocosta2/Xiaozhi_Custom_Portuguese/main/MicroWakeWords/models/v2/ola_xiaozhi.json
```

### 4. Referências de modelos da comunidade
- [RealDeco/xiaozhi-esphome MicroWakeWords](https://github.com/RealDeco/xiaozhi-esphome/tree/main/MicroWakeWords) — `hey_sarah`
- [JohnnyPrimus/Custom_V2_MicroWakeWords](https://github.com/JohnnyPrimus/Custom_V2_MicroWakeWords) — `computer`, `hey_friday`
- [esphome/micro-wake-word-models](https://github.com/esphome/micro-wake-word-models) — experimentais (`hey_home_assistant`, `okay_computer`, ...)

## Notas
- Os ficheiros `.json` precisam de `"version": 2` para funcionar no ESPHome 2026.7+.
- Se o modelo rebentar memória, aumenta `tensor_arena_size` no `.json` (ex.: 30000).
