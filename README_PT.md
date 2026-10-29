# XIAOZHI-HOME ASSISTANT

Integre os seus dispositivos Xiaozhi AI ao ESPHome e transforme-os em assistentes de voz para o Home Assistant.

(funcionalidade completa com reconhecimento de palavra-chave local e elementos gráficos personalizados.)

> ⚠️ Este projeto está baseado no [RealDeco/xiaozhi-esphome](https://github.com/RealDeco/xiaozhi-esphome). O que o distingue são as **imagens personalizadas** (8 personagens) e os **relógios/wallpapers** já incluídos neste repositório.

---

## 📁 Estrutura

```
Devices/
  Modular/                    # ⭐ Versão recomendada (versão modular v1.12)
    Ball v2.yaml              # Spotpear Ball v2
    Ball v1.yaml              # Spotpear Ball v1
    Muma.yaml                 # Spotpear Muma Box
    EchoEar.yaml              # EchoEar v1.2
    Breadboard_DIY_2.4.yaml   # Breadboard DIY (240x320)
    esp32-s3-box-3.yaml       # ESP32-S3-BOX-3 (320x240)
    Freenove-2.8.yaml         # Freenove ESP32S3 2.8" (240x320)
    Lichuang_s3_cam.yaml      # Lichuang S3 CAM (240x320)
    Waveshare_Audio_Board.yaml# Waveshare Audio Board (240x240)
    Waveshare_1.85C.yaml      # Waveshare 1.85C / 1.85C-BOX (360x360)
    Waveshare_1.85C_v1-2.yaml # Waveshare 1.85C v2 / 1.85C-BOX v2 (360x360)
    Guition_Taichi_Pi_V1.yaml # Guition Taichi Pi V1 (360x360)
    Guition_Taichi_Pi_V2.yaml # Guition Taichi Pi V2 (360x360, micro PDM)
    Xingzhi_Cube_1.54.yaml    # Xiaozhi Cube 1.54 (240x240)
    Xingzhi_Cube_1.83_2mic.yaml # Xingzhi Cube 1.83 2mic (284x240)
    "Ball v2 SENDSPIN.yaml"   # Music Assistant (experimental)
    localtest/                # Packages locais (core, display_pages, clocks, HW)
      core.yaml               #   Lógica central do assistente
      core-sendspin.yaml      #   Variante SENDSPIN
      display_pages.yaml      #   Páginas do ecrã (emoções, timer, ...)
      clocks-*.yaml           #   Estilos de relógio
      HW/*.yaml               #   Definições de hardware por dispositivo
  SpotPear Ball/
    Ball v2.yaml             # Versão "standalone" antiga (ficheiro único)
images/
  <Modelo>/240x240/          # Ilustrações do personagem (loading, idle, listening, ...)
  <Modelo>/240x320/          # Versões para ecrãs 240x320 (Jarvis, Eyes, Mario, Prime)
  <Modelo>/360x360/          # Versões para ecrãs 360x360 (Jarvis, Eyes, Mario, Prime)
  <Modelo>/284x240/          # Versões para ecrãs 284x240 (Jarvis, Eyes, Mario, Prime)
  Other/240x240/             # Wallpapers para o relógio + imagens de erro
  Other/240x320/, 320x240/   # Wallpapers para ecrãs verticais/paisagem
sounds/                      # Sons de startup e notificações
setup.ps1                    # Script de setup/validação/compilação local (Windows)
MicroWakeWords/              # Documentação de wake words em português
HA_Automations/              # Automações prontas (em português)
```

**Opções de `imagemodel`:** `Jarvis`, `Eyes`, `Mario`, `Prime`, `Steve`, `Brian`, `BumbleBee`, `Goku`
**Nota 240x320:** só `Jarvis`, `Eyes`, `Mario` e `Prime` têm versões nativas 240x320. Nesses ecrãs, para usar os outros modelos muda `imageheight` para `"240"` (a imagem é esticada).
**Nota 360x360:** só `Jarvis`, `Eyes`, `Mario` e `Prime` têm versões nativas 360x360 (Waveshare 1.85C / 1.85C v2 e Guition Taichi Pi V1/V2). Para os outros modelos, usa um dispositivo de 240x240.
**Nota 284x240:** só `Jarvis`, `Eyes`, `Mario` e `Prime` têm versões 284x240 (Xingzhi 1.83 2mic), redimensionadas a partir das fontes 480x480.

---

## 🚀 Guia de Início Rápido (Versão Modular — Recomendada)

### Requisitos
- ESPHome **2026.7.0 ou superior**.
- Os **packages são locais** (pasta `Devices/Modular/localtest/`) — nenhuma dependência externa ao RealDeco.
- As imagens e sons são servidos a partir deste repositório (GitHub raw).

### Como Instalar
1. Ligue o dispositivo ao computador via cabo USB. Aceda ao ESPHome Web, clique em **NEW DEVICE** e siga os passos para configurar e conectar à rede Wi-Fi.
2. No ESPHome, adote o dispositivo recém-detetado, edite a configuração e **cole o código do `Ball v2.yaml`** (pasta `Devices/Modular/`).
   - Altere o `name` e o `friendly_name` ao seu gosto.
   - Escolha o `imagemodel` pretendido (ex.: `"Goku"`, `"Jarvis"`).
   - Preencha as entidades de presença/luzes e a entidade de tempo nas **SETTINGS** (só são usadas pelo relógio estilo "Presence" e pelo relógio de tempo — se não as usar, pode ignorar).
3. Grave e instale o firmware. Espere que o dispositivo reinicie e execute o novo código.
4. Quando estiver visível no Home Assistant, vá a **Dispositivos** e confirme o novo dispositivo para iniciar a configuração do assistente de voz.

> 💡 **Nota sobre o método de instalação:** O ESPHome Web/Cloud descarrega o repositório inteiro, pelo que os `!include` relativos (`localtest/`) e as imagens/sons funcionam sem configuração extra.

### Atualizar para uma nova versão do Modular
Substitua os ficheiros em `Devices/Modular/localtest/` pelos novos do RealDeco:
https://github.com/RealDeco/xiaozhi-esphome/tree/main/devices/Under_Development/Modular
Depois recompila. Como o `core.yaml` usa `min_version: 2026.7.0`, mantenha o ESPHome atualizado.

### Nota importante para o Passo 3
Se a instalação por Wi-Fi não for bem-sucedida e for sugerida a utilização de USB:

- Volte a ligar o dispositivo via cabo, se necessário.
- Clique em instalar novamente, selecione **"Plug into this computer"**, espere o firmware ser compilado, descarregue-o e utilize o ESPHome Web para gravá-lo por USB.
- Isso é necessário apenas na primeira vez para ajustar as partições. As atualizações seguintes poderão ser feitas por Wi-Fi.

Se mesmo assim ainda não funcionar, tente desligar o dispositivo e ligar sem largar o botão de power — isso fará com que ele fique em modo **BOOT** e já deixe instalar (recomendo não largar o botão durante todo o processo, que leva cerca de 2 a 3 minutos).

### Firmware pré-compilado (CI)
O workflow **Build Firmware** (`.github/workflows/build-firmware.yml`) compila todos os YAMLs de `Devices/Modular/` e disponibiliza os `.bin` como *artifacts*. Para usar:
1. Vai a **Actions → Build Firmware → Run workflow** (branch `main`).
2. No final, descarrega o artifact `firmware-<dispositivo>` de cada job.
3. Grava via ESPHome Web → **Install** → manual file, ou o instalador Web do dispositivo.
Gera `*.factory.bin` (flash inicial, partições) e `*.ota.bin` (atualização por Wi-Fi).

### Desenvolvimento local (Windows)
Usa o script `setup.ps1` na raiz do repositório:
```powershell
.\setup.ps1                          # cria venv + instala ESPHome (1ª vez)
.\setup.ps1 -Validate                # valida todos os configs (esphome config)
.\setup.ps1 -Compile -Config "Devices/Modular/Ball v2.yaml"
.\setup.ps1 -UpdateEsphome
```
> ⚠️ **MAX_PATH do Windows:** se a compilação falhar com erros de caminho (`.esphome/build/...` muito longo), copia a pasta do repositório para um caminho curto (ex.: `C:\xz`) e corre de lá.

### Music Assistant (SENDSPIN)
O `Ball v2 SENDSPIN.yaml` é a variante experimental com Music Assistant: album art, multiroom e controlos de reprodução no ecrã (swipes = próxima/anterior faixa e volume). Requer ESPHome 2026.7.0+, o componente experimental `github://pr#16057` e um Music Assistant configurado no HA.

### Funcionalidades da versão Modular
- **Relógios no ecrã** quando o dispositivo está idle (7-segment, Flip, Default, Presence, Weather, Analog, Wide, Big, Xiaozhi...).
- **Wallpapers** de relógio selecionáveis a partir do Home Assistant.
- **Bateria**: sensor de tensão ADC + percentagem calibrada, com indicador no ecrã (ativável por switch).
- **Touchscreen**: toque = start/stop do assistente; **swipes** (esquerda/direita trocam o estilo do relógio, cima muda o wallpaper, baixo alterna a bateria) — expostos também como sensores no HA.
- **Sons**: startup (ao ligar ao HA) e wake sound (ao detetar a palavra-chave), com switches no HA.
- **Sensores de texto** com eventos (phase_id, stt_text, tts_text, tts_uri) para automações.
- **Relógio com presença por divisão** e relógio meteorológico (requer configurar as entidades nas SETTINGS).

---

## 🤖 Automações (pasta `HA_Automations/`)
Exemplos prontos em português: swipes (trocar relógio/wallpaper), mostrar pedido/resposta no dashboard.
Lê o cabeçalho de cada ficheiro para instruções (substituir o nome do dispositivo, criar helpers).

## 🗣️ Wake Word em português
Sem modelo público pré-treinado. Instruções para treinar o teu (`MicroWakeWords/README_PT.md`).

---

## 🚀 Guia de Início Rápido (Versão Standalone — `Ball v2.yaml`)

Versão antiga em ficheiro único, sem bateria/touchscreen/relógios. Mantida apenas por compatibilidade. O processo de instalação é idêntico ao acima; basta colar o conteúdo do `Ball v2.yaml` (pasta `Devices/SpotPear Ball/`).

---

## ✅ Modelos Compatíveis (até o momento)

- Spotpear Ball v2 (recomendado)
- Spotpear Ball v1
- Spotpear Muma Box
- EchoEar v1.2
- Breadboard DIY 2.4
- ESP32-S3-BOX-3
- Freenove ESP32S3 2.8"
- Lichuang S3 CAM
- Waveshare Audio Board
- Waveshare 1.85C
- Waveshare 1.85C v2
- Guition Taichi Pi V1
- Guition Taichi Pi V2
- Xiaozhi Cube 1.54
- Xingzhi Cube 1.83 2mic

---

## 🛠️ Troubleshooting

| Problema | Solução |
|---|---|
| `Could not download from .../images/...` | Verifica se o ficheiro existe no GitHub (as imagens são servidas de `raw/main`). Depois de adicionares uma imagem, faz push antes de compilar. |
| Erro `min_version` ao validar | Atualiza o ESPHome para 2026.7.0+ (`pip install -U esphome` ou no Web). |
| `unacceptable character` ao editar ficheiros no Windows | Não guardes o `core.yaml` com PowerShell/Bloco de Notas (corrompe os caracteres CJK). Usa um editor que respeite UTF-8 ou recopia o ficheiro original. |
| Erro de memória ao compilar | Usa menos wake words (comenta `hey_mycroft`/`alexa`) ou troca para um modelo de imagem mais simples. |
| `Not a valid model name ... for custom wake word` | Confirma que o `.json` do modelo tem `"version": 2`. |
| O relógio não aparece | Ativa o switch "Clock Screensaver" e verifica se não há timer ativo. O atraso é configurável em "Clock Screensaver Delay". |
| Swipes não funcionam | Desliga o switch "Handle swipes on device" no dispositivo se usares automações externas. |
| Entidades de presença/clima não atualizam | Confirma que os entity_id nas SETTINGS existem no HA e que o dispositivo está ligado ao HA. |
