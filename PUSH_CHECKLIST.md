# SSH / PUSH чек-лист (новая сессия Termux)

```bash
# 1. Перейти в папку проекта
cd ~/ai-tutor-course

# 2. Загрузить ключ в агент (пароль ключа ввести 1 раз за сессию)
eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_denis_kaa

# 3. Проверить, что ключ загружен
ssh-add -l

# 4. Проверить, что нет лишних изменений и пути чистые
git status --short | grep -v '^??'
git ls-files | awk -F/ '{print $1}' | sort -u

# 5. Пушить
git push origin main
```

## Если `Permission denied (publickey)`:
```bash
# Вариант А: явное указание ключа без агента
GIT_SSH_COMMAND="ssh -i ~/.ssh/id_denis_kaa -o IdentitiesOnly=yes" git push origin main

# Вариант Б: проверить, что ключ добавлен в аккаунт Denis-kaa
cat ~/.ssh/id_denis_kaa.pub
# скопировать вывод -> https://github.com/settings/keys (аккаунт Denis-kaa)
```

## Важно:
- НЕ делать `git add .` из home.
- НЕ коммитить node_modules/, dist/, .env, .git-credentials (они в .gitignore).
- Секреты — только через `pass` (GPG), никогда в коде.
