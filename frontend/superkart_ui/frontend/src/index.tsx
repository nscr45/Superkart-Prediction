import { StrictMode } from "react";
import { createRoot, type Root } from "react-dom/client";
import type {
  FrontendRenderer,
  FrontendRendererArgs,
} from "@streamlit/component-v2-lib";
import PredictionReveal, { type PredictionRevealData } from "./PredictionReveal";
import "./styles.css";

const roots = new WeakMap<HTMLElement, Root>();

const PredictionRevealRoot: FrontendRenderer<
  Record<string, never>,
  PredictionRevealData
> = (args: FrontendRendererArgs<Record<string, never>, PredictionRevealData>) => {
  const { data, parentElement } = args;
  const mount = parentElement.querySelector<HTMLElement>(".superkart-react-root");

  if (!mount) {
    throw new Error("SuperKart prediction component mount point was not found.");
  }

  let root = roots.get(parentElement);
  if (!root) {
    root = createRoot(mount);
    roots.set(parentElement, root);
  }

  root.render(
    <StrictMode>
      <PredictionReveal
        prediction={data.prediction}
        mrp={data.mrp}
        product_id={data.product_id}
      />
    </StrictMode>,
  );

  return () => {
    const mountedRoot = roots.get(parentElement);
    if (mountedRoot) {
      mountedRoot.unmount();
      roots.delete(parentElement);
    }
  };
};

export default PredictionRevealRoot;
