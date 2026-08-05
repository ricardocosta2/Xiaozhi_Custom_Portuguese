# XIAOZHI-HOME ASSISTANT

Integre os seus dispositivos Xiaozhi AI ao ESPHome e transforme-os em assistentes de voz para o Home Assistant.

(funcionalidade completa com reconhecimento de palavra-chave local e elementos gráficos personalizados.)

> ⚠️ Este projeto está baseado no [RealDeco/xiaozhi-esphome](https://github.com/RealDeco/xiaozhi-esphome). O que o distingue são as **imagens personalizadas** (8 personagens) e os **relógios/wallpapers** já incluídos neste repositório.

---

## 📁 Estrutura

```
Devices/
  SpotPear Ball/
    Ball v2.yaml             # Versão "standalone" (ficheiro único, antiga)
    Ball v2 Modular.yaml     # ⭐ Versão recomendada (modular, usa packages)
images/
  <Modelo>/240x240/          # Ilustrações do personagem (loading, idle, listening, ...)
  Other/240x240/             # Wallpapers para o relógio
```

**Opções de `imagemodel`:** `Jarvis`, `Eyes`, `Mario`, `Prime`, `Steve`, `Brian`, `BumbleBee`, `Goku`

---

## 🚀 Guia de Início Rápido (Versão Modular — Recomendada)

### Requisitos
- ESPHome **2026.7.0 ou superior**.
- Conexão à internet durante a compilação (o *core* é descarregado do GitHub do RealDeco).

### Como Instalar
1. Ligue o dispositivo ao computador via cabo USB. Aceda ao ESPHome Web, clique em **NEW DEVICE** e siga os passos para configurar e conectar à rede Wi-Fi.
2. No ESPHome, adote o dispositivo recém-detetado, edite a configuração e **cole o código do `Ball v2 Modular.yaml`**.
   - Altere o `name` e o `friendly_name` ao seu gosto.
   - Escolha o `imagemodel` pretendido (ex.: `"Goku"`, `"Jarvis"`).
   - Preencha as entidades de presença/luzes e a entidade de tempo nas **SETTINGS** (só são usadas pelo relógio estilo "Presence" e pelo relógio de tempo — se não as usar, pode ignorar).
3. Grave e instale o firmware. Espere que o dispositivo reinicie e execute o novo código.
4. Quando estiver visível no Home Assistant, vá a **Dispositivos** e confirme o novo dispositivo para iniciar a configuração do assistente de voz.

### Nota importante para o Passo 3
Se a instalação por Wi-Fi não for bem-sucedida e for sugerida a utilização de USB:

- Volte a ligar o dispositivo via cabo, se necessário.
- Clique em instalar novamente, selecione **"Plug into this computer"**, espere o firmware ser compilado, descarregue-o e utilize o ESPHome Web para gravá-lo por USB.
- Isso é necessário apenas na primeira vez para ajustar as partições. As atualizações seguintes poderão ser feitas por Wi-Fi.

Se mesmo assim ainda não funcionar, tente desligar o dispositivo e ligar sem largar o botão de power — isso fará com que ele fique em modo **BOOT** e já deixe instalar (recomendo não largar o botão durante todo o processo, que leva cerca de 2 a 3 minutos).

### Funcionalidades da versão Modular
- **Relógios no ecrã** quando o dispositivo está idle (7-segment, Flip, Default, Presence, Weather, Analog, Wide, Big, Xiaozhi...).
- **Wallpapers** de relógio selecionáveis a partir do Home Assistant.
- **Bateria**: sensor de tensão ADC + percentagem calibrada, com indicador no ecrã (ativável por switch).
- **Touchscreen**: toque = start/stop do assistente; **swipes** (esquerda/direita trocam o estilo do relógio, cima muda o wallpaper, baixo alterna a bateria) — expostos também como sensores no HA.
- **Sons**: startup (ao ligar ao HA) e wake sound (ao detetar a palavra-chave), com switches no HA.
- **Sensores de texto** com eventos (phase_id, stt_text, tts_text, tts_uri) para automações.
- **Relógio com presença por divisão** e relógio meteorológico (requer configurar as entidades nas SETTINGS).

---

## 🚀 Guia de Início Rápido (Versão Standalone — `Ball v2.yaml`)

Versão antiga em ficheiro único, sem bateria/touchscreen/relógios. Mantida apenas por compatibilidade. O processo de instalação é idêntico ao acima; basta colar o conteúdo do `Ball v2.yaml`.

---

## ✅ Modelos Compativeis (até o momento)

- Spotpear Ball v2
