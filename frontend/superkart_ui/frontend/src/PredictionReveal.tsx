import { useEffect, useMemo, useState } from "react";

export type PredictionRevealData = {
  prediction: number;
  mrp: number;
  product_id: string;
  run_id: string;
};

type Props = PredictionRevealData;

const formatCurrency = (value: number) =>
  new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);

export default function PredictionReveal({
  prediction,
  mrp,
  product_id,
  run_id,
}: Props) {
  const [displayValue, setDisplayValue] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [detailsOpen, setDetailsOpen] = useState(false);

  const multiple = useMemo(
    () => (mrp > 0 ? prediction / mrp : 0),
    [prediction, mrp],
  );

  useEffect(() => {
    let frame = 0;
    let startTime = 0;
    const duration = 850;
    setDisplayValue(0);
    setRevealed(false);

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplayValue(prediction * eased);

      if (progress < 1) {
        frame = window.requestAnimationFrame(animate);
      } else {
        setRevealed(true);
      }
    };

    frame = window.requestAnimationFrame(animate);
    return () => window.cancelAnimationFrame(frame);
  }, [prediction, product_id, run_id]);

  return (
    <section className={`sk-result-card ${revealed ? "is-revealed" : ""}`}>
      <div className="sk-result-topline">
        <span className="sk-result-label">MODEL PREDICTION</span>
        <span className="sk-result-status">Completed</span>
      </div>
      <div className="sk-result-value" aria-live="polite">
        {formatCurrency(displayValue)}
      </div>
      <div className="sk-result-caption">
        Predicted sales for product <strong>{product_id}</strong>
      </div>
      <div className="sk-result-divider" />
      <div className="sk-result-support">
        <div>
          <span className="sk-support-label">Product MRP</span>
          <strong>{formatCurrency(mrp)}</strong>
        </div>
        <div>
          <span className="sk-support-label">Sales / MRP multiple</span>
          <strong>{multiple.toFixed(2)}x</strong>
        </div>
      </div>
      <button
        className="sk-details-button"
        type="button"
        aria-expanded={detailsOpen}
        onClick={() => setDetailsOpen((open) => !open)}
      >
        {detailsOpen ? "Hide calculation note" : "View calculation note"}
        <span aria-hidden="true">{detailsOpen ? "−" : "+"}</span>
      </button>
      {detailsOpen && (
        <p className="sk-result-note">
          Sales / MRP is a descriptive ratio of the model prediction to the
          product's listed retail price. It is not a profit margin or a
          measure of store profitability.
        </p>
      )}
    </section>
  );
}
