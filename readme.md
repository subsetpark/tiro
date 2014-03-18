# Abba: The Abbreviation engine

`abba` is a full-featured 'abbreviation engine' written in Python 3. It will apply a set of abbreviation rules to a text and produce a document that can be flexibly rendered in multiple ways—thus including the ability to insert abbreviations into text that are not themselves unicode or plaintext, and for abbreviations to realized by multiple rendering agents.

## Abbreviation rules

Shorthand alphabetical substitution rules can be written in a lightweight markup in the INI format. For instance, here is a single sample rule:
``` .ini
[AND]
pattern: and#iso
uni_rep: {204a}
```
Which looks for occurances of the word 'and' by itself and then replaces it with an abbreviation of the user's choosing. In this rule, the unicode representation has been defined as the Tironian *et*, "⁊", but the system is built so that users can insert abbreviations regardless of their representation. Thus, they are not bound by the unicode character set. This sample rule:
``` .ini
[O_ND]
pattern: nd#vow
uni_rep: {036b}
```
Abbreviaties the characters 'nd' whenever they are found after a vowel. But not, for instance, after the number 2.

## Abbreviation

`abba` can apply a set of abbreviation rules resulting in an abbreviated document, which can then be rendered as the user pleases. Currently the application supports rendering to unicode text. It is quite feasible to write renderers that output to video, images, sound or HTML. Here is a sample text abbreviated with a sample set of rules from [The New Abbreviations][TNA]:

> Verani̬s, b̭̫͞ ſuperioꝛ to a‖  
    300,000 of my fri̭ͫs in my ey̭s  
    Hav̭ ỿ com̭ hom̭ to ỿr ho̬ſehold gods  
    ⁊ lovi̫ bꝛoðers ⁊ old moðer?  
    ỿv̭ com̭ back! o happy news foꝛ m̃!  
    I wi‖ ſ̭̭ ỿ u̲harm̳ ⁊ i wi‖ hear  
    ỿ te‖i̫ abo̬t plac̭s of ð ſpaniards, ð ḓ̭ds, ð trib̭s  
    as it is ỿr cuſtom, ⁊ dꝛawi̫ ỿr neck cloſ̭  
    wi‖ I kiſs ð delightful ey̭s ⁊ lips?  
    O how many happy men ðr ar̭,  
    Ⱳo is happi̭r ⁊ moꝛ̭ bḽſſ̳ ðan I am?

[TNA]: https://thoughtstreams.io/zdsmith/new-abbreviations/

## Generator mode

`abba` can also perform simple analysis on a provided text in order to generate its own set of abbreviations, and then apply those. Here is a sample text with dynamically generated abbrevations:

> Prut, tut, ϵ Ў, whϕ doɻ ζ fool ϘѮ Ǽ ҏy? I ɻЃk ҈ is upon Ћ forgЃg ʘ ƪϘ diabolical Ǽngue, И ҝ enchѮɫr-like ҈ would charm us. Ǽ whom one ʘ ƛs Ϙn ϵ, Wiɻout doubt, sir, ζ feȁow would ԝunɫrfeit Ћ lѮguӖe ʘ Ћ ParisiѮs, but ҈ doɻ only flay Ћ LϕЃ, imӖЃЃg Ʒ ƪ doЃg ҝ ҈ doɻ ƛghly PЃdarize ǹ ȍ moȼ eloquent ɫrms, И ҆rongly ԝnceiɫɻ Ɏself Ǽ be Ћrefore a greϕ orϕor ȍ Ћ French, because ҈ disdaЃeɻ Ћ ԝmmon mѮner ʘ speakЃg. Ǽ ϰ Ў ϵ, Is ǹ true? Ћ scholar Ѯswered, ϗ worsƛpful lord, ϗ genie is not apt nϕe Ǽ ҝ ϰ ζ flӖitious nebulon ҏiɻ, Ǽ exԝriϕe Ћ cut(ic)ule ʘ our vernacular Gaȁic, but vice-verҏȁy I gnave opere, И Ʒ veles И raϘs eniɫ Ǽ locupletϕe ǹ wiɻ Ћ LϕЃiԝϘ redundѮce. Ʒ G—, ϵ Ў, I wiȁ ɫach you Ǽ speak. But firȼ ԝϘ ƛɻer, И ɫȁ Ϙ wԉnce ε art. Ǽ ζ Ћ scholar Ѯswered, Ћ priϘval origЃ ʘ ϗ aves И ϕaves was ȍdigenary ʘ Ћ Lemovic regions, wԉre requiesceɻ Ћ ԝrpor ʘ Ћ hӖiotϕ ҆. Martial. I underȼѮd ΰ very weȁ, ϵ Ў. Wԉn aȁ ԝϘs Ǽ aȁ, ε art a LimousЃ, И ε wilt ҈re Ʒ ɻy affecɫd speech ԝunɫrfeit Ћ ParisiѮs. Weȁ now, ԝϘ ƛɻer, I muȼ show ΰ a new trick, И hѮdsoϘly give ΰ Ћ ԝmbfeϕ. Wiɻ ζ ҈ Ǽok Ɏ Ʒ Ћ ɻroϕ, ҏyЃg Ǽ Ɏ, ε flayeȼ Ћ LϕЃ; Ʒ ҆. John, I wiȁ make ΰ flay Ћ fox, for I wiȁ now flay ΰ alive. Ћn begѮ Ћ poor LimousЃ Ǽ cry, Haw, gwid maasɫr! haw, Laord, ϗ halp, И ҆. Marshaw! haw, I'm worried. Haw, ϗ ɻropple, Ћ beѮ ʘ ϗ crӖg is bruck! Haw, for gauad's seck lawt ϗ leѮ, mawsɫr; waw, waw, waw. Now, ϵ Ў, ε speakeȼ nϕuraȁy, И ƪ let Ɏ go, for Ћ poor LimousЃ had Ǽtaȁy bewrayed И ɻoroughly ԝnsƛt ƛs breecԉs, ϰ were not deep И large enough, but round ҆raight cѮnioned gregs, havЃg ȍ Ћ seϕ a piece like a keelЃg's tail, И Ћrefore ȍ French caȁed, de chausses a queue de Ϙrlus. Ћn, ϵ Ў, ҆. AlipѮtЃ, whϕ civet? Fie! Ǽ Ћ devil wiɻ ζ turnip-eϕer, ʉ ҈ ҆Ѓks! И ƪ let Ɏ go. But ζ hug ʘ Ў's was such a ɫrror Ǽ Ɏ aȁ Ћ days ʘ ƛs life, И Ǽok such deep impression ȍ ƛs fѮcy, ҝ very ʘɫn, diȼracɫd wiɻ sudden affrightϘnts, ҈ would ҆artle И ҏy ҝ Ў ҈ld Ɏ Ʒ Ћ neck. Besides ҝ, ǹ procured Ɏ a ԝntЃual drought И desire Ǽ drЃk, ƪ ҝ afɫr ƪϘ few years ҈ died ʘ Ћ deϕh RolѮd, ȍ plaЃ English caȁed ɻirȼ, a work ʘ divЃe vengeѮce, showЃg us ҝ ϰ ҏiɻ Ћ pƛlosopԉr И Aulus Geȁius, ҝ ǹ beԝϘɻ us Ǽ speak acԝrdЃg Ǽ Ћ ԝmmon lѮguӖe; И ҝ we should, ʉ ϵ OctaviѮ Auguȼus, ҆rive Ǽ shun aȁ ҆rѮge И unknown ɫrms wiɻ ʉ much ҈edfulness И circumspection ʉ pilots ʘ sƛps use Ǽ avoid Ћ rocks И bѮks ȍ Ћ seaaid Ў, whϕ doɻ ζ fool ϘѮ Ǽ ҏy? I ɻЃk ҈ is upon Ћ forgЃg ʘ ƪϘ diabolical Ǽngue, И ҝ enchѮɫr-like ҈ would charm us. Ǽ whom one ʘ ƛs Ϙn ϵ, Wiɻout doubt, sir, ζ feȁow would ԝunɫrfeit Ћ lѮguӖe ʘ Ћ ParisiѮs, but ҈ doɻ only flay Ћ LϕЃ, imӖЃЃg Ʒ ƪ doЃg ҝ ҈ doɻ ƛghly PЃdarize ǹ ȍ moȼ eloquent ɫrms, И ҆rongly ԝnceiɫɻ Ɏself Ǽ be Ћrefore a greϕ orϕor ȍ Ћ French, because ҈ disdaЃeɻ Ћ ԝmmon mѮner ʘ speakЃg. Ǽ ϰ Ў ϵ, Is ǹ true? Ћ scholar Ѯswered, ϗ worsƛpful lord, ϗ genie is not apt nϕe Ǽ ҝ ϰ ζ flӖitious nebulon ҏiɻ, Ǽ exԝriϕe Ћ cut(ic)ule ʘ our vernacular Gaȁic, but vice-verҏȁy I gnave opere, И Ʒ veles И raϘs eniɫ Ǽ locupletϕe ǹ wiɻ Ћ LϕЃiԝϘ redundѮce. Ʒ G—, ϵ Ў, I wiȁ ɫach you Ǽ speak. But firȼ ԝϘ ƛɻer, И ɫȁ Ϙ wԉnce ε art. Ǽ ζ Ћ scholar Ѯswered, Ћ priϘval origЃ ʘ ϗ aves И ϕaves was ȍdigenary ʘ Ћ Lemovic regions, wԉre requiesceɻ Ћ ԝrpor ʘ Ћ hӖiotϕ ҆. Martial. I underȼѮd ΰ very weȁ, ϵ Ў. Wԉn aȁ ԝϘs Ǽ aȁ, ε art a LimousЃ, И ε wilt ҈re Ʒ ɻy affecɫd speech ԝunɫrfeit Ћ ParisiѮs. Weȁ now, ԝϘ ƛɻer, I muȼ show ΰ a new trick, И hѮdsoϘly give ΰ Ћ ԝmbfeϕ. Wiɻ ζ ҈ Ǽok Ɏ Ʒ Ћ ɻroϕ, ҏyЃg Ǽ Ɏ, ε flayeȼ Ћ LϕЃ; Ʒ ҆. John, I wiȁ make ΰ flay Ћ fox, for I wiȁ now flay ΰ alive. Ћn begѮ Ћ poor LimousЃ Ǽ cry, Haw, gwid maasɫr! haw, Laord, ϗ halp, И ҆. Marshaw! haw, I'm worried. Haw, ϗ ɻropple, Ћ beѮ ʘ ϗ crӖg is bruck! Haw, for gauad's seck lawt ϗ leѮ, mawsɫr; waw, waw, waw. Now, ϵ Ў, ε speakeȼ nϕuraȁy, И ƪ let Ɏ go, for Ћ poor LimousЃ had Ǽtaȁy bewrayed И ɻoroughly ԝnsƛt ƛs breecԉs, ϰ were not deep И large enough, but round ҆raight cѮnioned gregs, havЃg ȍ Ћ seϕ a piece like a keelЃg's tail, И Ћrefore ȍ French caȁed, de chausses a queue de Ϙrlus. Ћn, ϵ Ў, ҆. AlipѮtЃ, whϕ civet? Fie! Ǽ Ћ devil wiɻ ζ turnip-eϕer, ʉ ҈ ҆Ѓks! И ƪ let Ɏ go. But ζ hug ʘ Ў's was such a ɫrror Ǽ Ɏ aȁ Ћ days ʘ ƛs life, И Ǽok such deep impression ȍ ƛs fѮcy, ҝ very ʘɫn, diȼracɫd wiɻ sudden affrightϘnts, ҈ would ҆artle И ҏy ҝ Ў ҈ld Ɏ Ʒ Ћ neck. Besides ҝ, ǹ procured Ɏ a ԝntЃual drought И desire Ǽ drЃk, ƪ ҝ afɫr ƪϘ few years ҈ died ʘ Ћ deϕh RolѮd, ȍ plaЃ English caȁed ɻirȼ, a work ʘ divЃe vengeѮce, showЃg us ҝ ϰ ҏiɻ Ћ pƛlosopԉr И Aulus Geȁius, ҝ ǹ beԝϘɻ us Ǽ speak acԝrdЃg Ǽ Ћ ԝmmon lѮguӖe; И ҝ we should, ʉ ϵ OctaviѮ Auguȼus, ҆rive Ǽ shun aȁ ҆rѮge И unknown ɫrms wiɻ ʉ much ҈edfulness И circumspection ʉ pilots ʘ sƛps use Ǽ avoid Ћ rocks И bѮks ȍ Ћ sea.

## Usage

```
usage: abba.py [-h] [-g] [--ruleset RULESET] [-i INFILE] [-t TEXT [TEXT ...]]
               [-r RENDER] [-l]

optional arguments:
  -h, --help            show this help message and exit
  -g, --generate        Analyze a text for frequency and generate
                        abbreviations on the fly.
  --ruleset RULESET     The ruleset to use. Uses The New Abbreviations if none
                        is supplied.
  -i INFILE, --infile INFILE
  -t TEXT [TEXT ...], --text TEXT [TEXT ...]
                        The text to operate on.
  -r RENDER, --render RENDER
                        Render method. Accepts 'unicode' or 'base'.
  -l, --legend          Print a legend at the top of the text.
  ```