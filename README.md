# Google Sheets Api

Проект разработан на Python версии 3.10.

* Синхронизация базы данных с документом [Google Sheet](https://docs.google.com/spreadsheets/d/13LcpN3xNXU0AGf9YI07CLy-DO3FDv3p9EO5VJpDJlHY/edit?usp=sharing)  
* Отправка уведолений в о заказах в [telegram канал](https://t.me/+NqaM3rD7gEtmMWRi)
* Данные для перевода $ в рубли обновляются каждые 3 часа по курсу ЦБ РФ.
* Frontend на React

## Установка и запуск

Клонировать репозиторий с Github.com, перейти внутрь проекта  
````
git clone https://github.com/Povarenskiy/google_sheets_api.git
cd google_sheets_api
````
Запустить docker compose
````
docker-compose up -d    # on windows
docker compose up -d    # on linux
````

## URL

Api для запроса информации по заказам: [http://localhost:8000/](http://localhost:8000/) 

Сайт: [http://localhost:3000/](http://localhost:3000/) 
