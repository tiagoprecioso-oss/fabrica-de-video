# Direitos: o que a fábrica pode usar (atualizado em 29/10/2026)

Resumo prático, não é parecer jurídico. As regras são das empresas e mudam: releia a fonte antes de lançar.

## A regra que vale para tudo: conteúdo reutilizado
Ter o direito de usar **não basta para monetizar**. YouTube, TikTok e Meta cortam a monetização de quem só reposta, **mesmo com permissão do dono**.
- YouTube: "This policy applies even if you have permission from the original creator." Passa quando "viewers can tell that there's a meaningful difference": comentário, crítica, narração, edição com narrativa própria. Shorts: clipes não editados de filmes/séries, reuploads e compilações sem nada original não entram na divisão de receita. ([reutilizado](https://support.google.com/youtube/answer/1311392) · [Shorts](https://support.google.com/youtube/answer/12504220))
- TikTok Creator Rewards: não paga conteúdo copiado ou "com pequenas modificações". Legenda, velocidade ou filtro não contam. Vídeo precisa ter 1 min ou mais. (fontes secundárias: findclout.com, cut.pro)
- Instagram (abr/2026): contas cuja maior parte do mês é repost perdem alcance; marca d'água e corte leve não contam. Facebook (jul/2025): reposts repetidos perdem monetização. ([PetaPixel](https://petapixel.com/2026/04/30/new-instagram-policies-target-reposted-content/) · [TechCrunch](https://techcrunch.com/2025/07/14/following-youtube-meta-announces-crackdown-on-unoriginal-facebook-content))

**Por isso a fábrica nunca posta corte puro:** todo corte entra num vídeo com a nossa camada (dados, legendas, narrativa, comentário, animação). Isso já é o que o motor faz.

## Mapa de fontes de vídeo (mais seguro → mais arriscado)
| # | Fonte | Pode monetizar? | Condição | Fonte da regra |
|---|---|---|---|---|
| 1 | Nossas animações (Remotion) e trilha `tools/trilha.py` | Sim | — | é nosso |
| 2 | **NASA** (vídeo, foto, áudio) | Sim | Crédito "NASA". Sem logo/selo, sem sugerir endosso, sem rosto de astronauta em promoção. Material de terceiros marcado fica de fora | [NASA](https://nasa.gov/nasa-brand-center/images-and-media) |
| 3 | **Blender Studio** (filmes abertos) | Sim, se CC BY | Crédito por filme. *Spring*: "© Blender Foundation \| cloud.blender.org/spring". Conferir a licença de cada filme | [Blender](https://studio.blender.org/remixing/) |
| 4 | **Domínio público** — EUA: filmes e desenhos até 1930 (2026: *All Quiet on the Western Front*, *Animal Crackers*, Betty Boop e Mickey de 1930, Pluto; 2025: *The Skeleton Dance*, *Blackmail*, Popeye de 1929). Brasil: audiovisual 70 anos após a divulgação | Sim | Só a versão original (restauração nova pode ter direitos). Cuidado com **marcas** (Betty Boop, Popeye, Mickey): nada de parecer produto oficial. Baixar da Library of Congress ou Prelinger e guardar a origem para contestar Content ID. Internet Archive não garante o status | [Duke 2026](https://cspd.law.duke.edu/publicdomainday/2026) · [2025](https://copyrightlately.com/public-domain-2025/) · Lei 9.610 art. 44 |
| 5 | Bancos grátis (Pixabay, Pexels, Mixkit Free) | Sim, como b-roll | Proibido repostar o clipe "puro". Sem marcas aparecendo. Não têm cultura pop | [Pixabay](https://pixabay.com/en/service/license/) · [Pexels](https://help.pexels.com/hc/en-us/articles/360042332714) |
| 6 | YouTube com licença **CC BY** e Wikimedia Commons | Sim, se a licença permitir uso comercial | Filtro "Creative Commons" na busca. Crédito (título, autor, link, licença) na tela e na descrição. CC BY-SA obriga o vídeo a ter a mesma licença — evitar | [YouTube CC](https://support.google.com/youtube/answer/2797468) |
| 7 | **Gameplay de jogos** (ver tabela abaixo) | Sim, para a maioria | A gravação precisa ser **nossa** ou do criador que autorizou. Nunca de outro canal | políticas abaixo |
| 8 | **Cortes autorizados** de streamers/podcasts (campeonatos de cortes) | Pelo prêmio da campanha, sim. AdSense: só com valor original e allowlist | Ver seção "Cortes autorizados" | — |
| 9 | Anime **Kadokawa** com diretriz de clipes (ex.: *Shield Hero* T4: até 4 min por episódio em review) | Só entrando no MCN da Kadokawa | Título a título | [ANN 02/08/2025](https://www.animenewsnetwork.com/interest/2025-08-02/kadokawa-issues-guidelines-for-sampling-clips-from-4-summer-anime/.227139) |
| 10 | **Trailers e press kits** de filmes, séries e games | Arriscado | Disney: só uso jornalístico. Netflix: proíbe uso em vídeo sem permissão escrita. Ubisoft e Nintendo proíbem repostar trailer. Content ID quase certo. Só trecho curto (3–5 s) dentro de comentário nosso, com crédito — base legal no Brasil: art. 46, III e VIII da Lei 9.610 (citação para crítica, pequenos trechos) | [Netflix](https://help.netflix.com/en/legal/media-terms-and-conditions) · [Games Press FAQ](https://gamespress.com/FAQ---Use-of-Assets) · [Lei 9.610](https://www.planalto.gov.br/ccivil_03/leis/l9610.htm) |
| 11 | Cenas de filmes, séries e animes atuais sem licença | **Não** | Strike e perda de monetização | — |
| 12 | Gameplay, lives ou cortes de outros canais sem autorização | **Nunca** | — | — |

## Games: quem deixa monetizar gameplay
Todas exigem conteúdo com criação nossa. Nenhuma libera trailer "puro".
| Empresa | Monetizar gameplay? | Aviso obrigatório / restrições | Política |
|---|---|---|---|
| Microsoft/Xbox (Bethesda, Activision Blizzard: não listados nominalmente) | Sim | "[Jogo] © Microsoft", feito sob as Game Content Usage Rules, não endossado. Sem logos, sem música licenciada de terceiros | [Xbox](https://www.xbox.com/en-US/developers/rules) |
| Minecraft | Sim, com conteúdo próprio | "NOT AN OFFICIAL MINECRAFT PRODUCT. NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT." | [Mojang](https://www.minecraft.net/en-us/usage-guidelines) |
| Nintendo | Sim, pelos programas listados (YouTube Partner, Meta…) | Exige "creative input and commentary". Trailers/Directs só com comentário. Não insinuar parceria | [Nintendo](https://www.nintendo.co.jp/networkservice_guideline/en/index.html) |
| Epic (Fortnite) | Sim | Aviso da Epic (abaixo). Sem skins de parceria, danças com música licenciada | [Epic](https://legal.epicgames.com/epicgames/fan-art-policy) |
| Riot (LoL, Valorant) | Sim, anúncios passivos | "Riot Games does not endorse or sponsor this project". Sem repostar VOD de esports | [Riot](https://www.riotgames.com/en/legal) |
| Valve (CS2, Dota) | Sim | Sem cobrar acesso, sem extrair assets | [Valve](https://store.steampowered.com/video_policy) |
| Ubisoft | Sim | **Proíbe repostar trailers**. Sem jogo inteiro | [Ubisoft](https://www.ubisoft.com/legal/documents/VideoPolicy/en-INTL) |
| EA | Sim | "Não é endossado pela EA". Sem conteúdo pré-lançamento | [EA](https://help.ea.com/pt-br/articles/security-and-rules/ea-content-policy/) |
| Capcom | Sim | Sem cutscene isolada, sem pré-lançamento, aviso de spoiler | [Capcom](https://www.capcomusa.com/video-policy/) |
| SEGA | Sim | Aviso de spoiler, sem música isolada. Atlus tem regra por jogo | [SEGA](https://www.sega.co.jp/en/streaming_guideline/) |
| Square Enix | Regra por jogo | Vídeo só de cenas é proibido. Copyright na tela | página de cada jogo |
| CD Projekt Red | Sim | "This is an unofficial fan work and is not approved/endorsed by CD PROJEKT RED." | [CDPR](https://cdprojektred.com/fan-content/) |
| Rockstar (GTA) | **Não** (só "non-commercial") | GTA só com nossas animações | [Rockstar](https://support.rockstargames.com/en-US/articles/7bNaeoMFTV0iUDGhStTXvz/policy-on-posting-copyrighted-rockstar-games-material) |
| Sony/PlayStation Studios, Bandai Namco, HoYoverse, Roblox | **Não confirmado** | Não usar até achar a política oficial | — |

## Cortes autorizados (streamers e podcasts)
Hoje a autorização vem quase toda de **campeonatos de cortes**: o criador libera um acervo, você corta, posta no seu perfil e recebe pelo prêmio ou por views.
- **Plataformas BR:** Viewx (Gaules, Gabepeixe, LOUD, Luquet4…, pagamento por ranking), Real Oficial / Real Rewards (Podpah, Yuri22, Wild Rift: R$ 1–1,75 por 1.000 views), Cut.Pro, Clipei. EUA: Whop Content Rewards (cada campanha define a taxa, ex.: US$ 3 por 1.000 views). Valores mudam toda semana.
- Só vale o **acervo oficial** da campanha. Trechos de filme, música ou esporte que aparecem na live **não** estão liberados.
- Autorização protege do Content ID **só** se o dono puser nosso canal na allowlist ([YouTube](https://support.google.com/youtube/answer/6070344)). **Não** protege da regra de conteúdo reutilizado.
- Antes de cortar: autorização por escrito (o quê, quais redes, pode monetizar?) guardada em `docs/autorizacoes/`.
- Casimiro e Inteligência Ltda têm canais de cortes próprios e não liberam terceiros. Flow: regras de 2021, não confirmadas hoje.

## Música
| Fonte | Pode? | Condição |
|---|---|---|
| Trilha sintetizada (`tools/trilha.py`) | Sim | É nossa. Padrão da fábrica. |
| Sascha Ende "Happy Beats / Business Moves" (CC BY 4.0) | Sim | Crédito no post: "Music: Sascha Ende, ende.app (CC BY 4.0)" |
| YouTube Audio Library, Pixabay Music, Mixkit | Depende | Conferir a licença de cada faixa (crédito, uso fora do YouTube) |
| Músicas em alta | Só no app | Escolher na biblioteca do TikTok/Instagram na hora de postar, nunca embutir no arquivo |
| Trilha original dos jogos, música de lives e trailers | Não | Tirar o áudio do clipe e usar a nossa trilha |

## Aviso obrigatório da Epic (descrição de todo vídeo com Fortnite)
> Portions of the materials used are trademarks and/or copyrighted works of Epic Games, Inc. All rights reserved by Epic. This material is not official and is not endorsed by Epic.

## Ainda não confirmado
Políticas de vídeo de Sony/PlayStation, Bandai Namco, HoYoverse e Roblox; licença de *Sintel*, *Big Buck Bunny* e *Charge* um a um; se restaurações em domínio público recebem Content ID; se um Short monetizado é "uso comercial" para a ESA (usar só itens CC BY-SA ou evitar).
