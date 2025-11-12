import { Link } from "react-router-dom";
import styles from "./Button.module.css";

export interface ButtonProps {
  type?: 'submit' | 'reset' | 'button';
  text?: string;
  href?: string;
  disabled?: boolean;
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  type,
  text,
  href,
  disabled,
  onClick,
}) => {
  const buttonComponent = <button
    type={type}
    disabled={disabled}
    className={styles.button}
    onClick={onClick}
  >
    {text}
  </button>

  return href
    ? <Link to={href}>{buttonComponent}</Link>
    : buttonComponent;
};