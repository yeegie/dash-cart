import { useState } from "react";
import styles from "./faq.module.css";

interface FaqItem {
  id: number;
  question: string;
  answer: string;
  category: string;
}

const faqData: FaqItem[] = [
  {
    id: 1,
    category: "Заказы",
    question: "Как отследить мой заказ?",
    answer: "После оформления заказа вы получите трекер номер на email и в личном кабинете. Вы можете отслеживать статус доставки в разделе 'Мои заказы'."
  },
  {
    id: 2,
    category: "Заказы",
    question: "Можно ли изменить состав заказа после оформления?",
    answer: "Изменения возможны в течение 1 часа после оформления заказа. Для этого свяжитесь с нашей службой поддержки."
  },
  {
    id: 3,
    category: "Доставка",
    question: "В какие города осуществляется доставка?",
    answer: "Мы доставляем заказы по всей России. Сроки и стоимость доставки зависят от вашего региона и выбранного способа доставки."
  },
  {
    id: 4,
    category: "Доставка",
    question: "Сколько стоит доставка?",
    answer: "Доставка бесплатна при заказе от 2000 рублей. При меньшей сумме стоимость доставки рассчитывается индивидуально для вашего региона."
  },
  {
    id: 5,
    category: "Оплата",
    question: "Какие способы оплаты вы принимаете?",
    answer: "Мы принимаем банковские карты (Visa, MasterCard, Мир), электронные кошельки (ЮMoney, Qiwi), а также наличные при получении."
  },
  {
    id: 6,
    category: "Оплата",
    question: "Безопасна ли оплата картой на сайте?",
    answer: "Да, все платежи защищены SSL-шифрованием. Мы не храним данные вашей карты - обработкой платежей занимается надежный платежный шлюз."
  },
  {
    id: 7,
    category: "Возврат",
    question: "Как вернуть товар?",
    answer: "Вы можете вернуть товар в течение 14 дней с момента получения. Товар должен сохранить товарный вид и оригинальную упаковку."
  },
  {
    id: 8,
    category: "Аккаунт",
    question: "Как восстановить доступ к аккаунту?",
    answer: "На странице входа нажмите 'Забыли пароль?' и следуйте инструкциям. Ссылка для восстановления будет отправлена на вашу почту."
  }
];

export const FaqPage = () => {
  const [activeCategory, setActiveCategory] = useState<string>("Все");
  const [searchTerm, setSearchTerm] = useState("");
  const [openItems, setOpenItems] = useState<number[]>([]);

  const categories = ["Все", ...new Set(faqData.map(item => item.category))];

  const toggleItem = (id: number) => {
    setOpenItems(prev => 
      prev.includes(id) 
        ? prev.filter(itemId => itemId !== id)
        : [...prev, id]
    );
  };

  const filteredFaq = faqData.filter(item => {
    const matchesCategory = activeCategory === "Все" || item.category === activeCategory;
    const matchesSearch = item.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.answer.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className={styles.faq}>
      <div className={styles.faq__header}>
        <h1 className={styles.faq__title}>Часто задаваемые вопросы</h1>
        <p className={styles.faq__subtitle}>
          Нашли ответы на самые популярные вопросы о работе нашего сервиса
        </p>
      </div>

      <div className={styles.faq__controls}>
        <div className={styles.search}>
          <input
            type="text"
            placeholder="Поиск по вопросам..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className={styles.search__input}
          />
        </div>

        <div className={styles.categories}>
          {categories.map(category => (
            <button
              key={category}
              className={`${styles.category__btn} ${
                activeCategory === category ? styles.category__btn_active : ""
              }`}
              onClick={() => setActiveCategory(category)}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      <div className={styles.faq__list}>
        {filteredFaq.length > 0 ? (
          filteredFaq.map(item => (
            <div key={item.id} className={styles.faq__item}>
              <button
                className={styles.faq__question}
                onClick={() => toggleItem(item.id)}
              >
                <span className={styles.faq__question_text}>
                  {item.question}
                </span>
                <span className={`${styles.faq__icon} ${
                  openItems.includes(item.id) ? styles.faq__icon_open : ""
                }`}>
                  ▼
                </span>
              </button>
              
              {openItems.includes(item.id) && (
                <div className={styles.faq__answer}>
                  <p>{item.answer}</p>
                </div>
              )}
            </div>
          ))
        ) : (
          <div className={styles.faq__empty}>
            <p>По вашему запросу ничего не найдено</p>
          </div>
        )}
      </div>

      <div className={styles.faq__support}>
        <h3>Не нашли ответ?</h3>
        <p>Наша служба поддержки всегда готова помочь вам</p>
        <div className={styles.support__contacts}>
          <a href="tel:+79991234567" className={styles.support__link}>
            📞 +7 (999) 123-45-67
          </a>
          <a href="mailto:support@dashcart.ru" className={styles.support__link}>
            ✉️ support@dashcart.ru
          </a>
        </div>
      </div>
    </div>
  );
};