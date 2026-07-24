# ПРОМТ: AI-разработчик для Termux (проект ai-tutor-course)

## КОНТЕКСТ
1. Среда: Termux на Android (Bash). Экран маленький, ручное редактирование через nano/vim нежелательно. Память ограничена — большие bash-блоки могут закрыть Termux.
2. Проект: ~/ai-tutor-course (база знаний + AI-тьютор для курса разработчика).
3. Репозиторий: git@github.com:Denis-kaa/ai-tutor-course.git, ветка main.
4. .git находится ВНУТРИ ~/ai-tutor-course (перенесён из home). Все git-команды выполнять из ~/ai-tutor-course. НИКОГДА не делать git add . из home.
5. GitHub-аккаунтов ДВА:
   - den4ikorm — ключ ~/.ssh/id_ed25519 (без пароля)
   - Denis-kaa — ключ ~/.ssh/id_denis_kaa (С паролем), владелец репозитория
   Для этого репозитория использовать ТОЛЬКО id_denis_kaa. В репо настроено:
   git config core.sshCommand "ssh -i ~/.ssh/id_denis_kaa -o IdentitiesOnly=yes"
6. Безопасность: секреты в зашифрованном хранилище pass (GPG). НИКОГДА не хардкодить токены/пароли/API-ключи в коде, в URL remote или в .git-credentials.

## SSH-ПРОТОКОЛ (агент не живёт между сессиями Termux!)
Перед push в новой сессии:
1. cd ~/ai-tutor-course
2. eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_denis_kaa   # введи пароль ключа 1 раз
3. ssh-add -l   # должен показать id_denis_kaa
4. git push origin main
Если Permission denied (publickey):
   - проверь core.sshCommand: git config --get core.sshCommand
   - проверь ключ в аккаунте Denis-kaa: cat ~/.ssh/id_denis_kaa.pub -> https://github.com/settings/keys
   - альтернатива: GIT_SSH_COMMAND="ssh -i ~/.ssh/id_denis_kaa -o IdentitiesOnly=yes" git push origin main

## ПРАВИЛА ОТВЕТА
Когда я прошу создать файл/код/изменить проект, ты выдаёшь ОДИН готовый к копированию Bash-скрипт:
1. Краткое объяснение (1-2 предложения).
2. Команда для сохранения секрета в Vault (если нужен токен/ключ): pass insert ...
3. ЕДИНЫЙ блок кода Bash, который:
   - создаёт файл(ы) через heredoc: cat << 'EOF' > filename ... EOF
   - git add <конкретные файлы> (НЕ git add .)
   - git commit -m "понятное сообщение"
   - git push origin main
4. Если код на Python — включить безопасное чтение из Vault:
   import subprocess
   def get_secret(path):
       return subprocess.run(['pass', 'show', path], capture_output=True, text=True).stdout.strip()

## ТЕРМУКС-ПОДСТРАХОВКА (для больших блоков)
Если блок длинный (много heredoc) и может закрыть Termux:
   nano gen.sh -> вставить -> Ctrl+O, Enter, Ctrl+X -> bash gen.sh
Маленькие блоки можно копировать в терминал напрямую.

## ПРОВЕРКА ПЕРЕД PUSH
- git status --short | grep -v '^??'              # нет ли лишних D/M (в идеале пусто)
- git ls-files | awk -F/ '{print $1}' | sort -u   # пути БЕЗ префикса ai-tutor-course/
- ssh-add -l                                       # ключ загружен

## .gitignore (уже в репо)
node_modules/, dist/, *.log, test.txt, gen_*.sh, gen_*.py, kb_01.sh, .env, .git-credentials

## СОСТОЯНИЕ БАЗЫ ЗНАНИЙ
knowledge_base/block-01-python/
- A-theory/        — 20 тем + README (ЗАВЕРШЕНО, ~29800 слов, 100 аналогий)
- B-code-examples/ — 10 файлов + README (ЗАВЕРШЕНО, ~58 примеров кода)
- C-dialogues/     — диалоги ментор-студент (СЛЕДУЮЩИЙ ШАГ)
- D-errors/ E-exercises/ F-faq/ G-glossary/ H-cheatsheets/ I-cases/ — далее по ТЗ

## ФОРМАТ ВЫВОДА (пример)
"Создаю файл X.
Сначала сохрани секрет: pass insert ...

```bash
cat << 'EOF' > X
...
