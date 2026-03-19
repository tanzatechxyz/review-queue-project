export function ActionButton({ label, onClick, tone = 'default', disabled = false }: { label: string; onClick?: () => void; tone?: 'default' | 'primary' | 'success' | 'danger'; disabled?: boolean }) {
  return <button className={`action-button ${tone}`} onClick={onClick} disabled={disabled}>{label}</button>
}
