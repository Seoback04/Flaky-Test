# UI Test Checklist — <Page / Flow>
## 1. Layout & Visual
- [ ] Renders correctly on supported breakpoints (mobile, tablet, desktop).
- [ ] No overlapping elements, truncated text, or clipped icons.
- [ ] Colors match design; sufficient contrast (WCAG AA).
- [ ] Images have `alt` text; icons have accessible names.
- [ ] Focus state is visible for every interactive element.
## 2. Functional
- [ ] Happy-path flow completes end-to-end.
- [ ] Form validation triggers on submit and on blur as specified.
- [ ] Required / optional fields match spec.
- [ ] Error messages are specific ("Password must be ≥ 8 chars"), not generic.
- [ ] Success states clearly acknowledged (toast / inline / redirect).
## 3. Negative
- [ ] Submit with empty required fields blocked.
- [ ] Submit with oversized inputs rejected.
- [ ] Paste of unsupported content handled gracefully.
- [ ] Network failure mid-submit → user kept informed, no silent loss.
- [ ] Auth expiry mid-session → redirect to re-auth; form state preserved where spec requires.
## 4. Accessibility (A11y)
- [ ] Keyboard-only navigation works for all interactive elements.
- [ ] `tab` order is logical.
- [ ] Screen reader announces form labels, errors, and status changes.
- [ ] No keyboard traps.
## 5. Browser / Device Matrix
- [ ] Chrome (latest, latest-1).
- [ ] Firefox (latest).
- [ ] Edge (latest).
- [ ] Safari (macOS latest).
- [ ] iOS Safari, Android Chrome.
## 6. State Persistence
- [ ] Back/forward navigation preserves state per spec.
- [ ] Refresh does not duplicate submissions.
- [ ] Session expiry has predictable behavior.
## 7. Performance
- [ ] Time to interactive under target (<Xs).
- [ ] No obvious layout thrash on interaction.
- [ ] Assets (fonts, images) use correct caching headers.
## 8. Observability
- [ ] Client errors reported to monitoring.
- [ ] Rage-click / error-click is captured.
- [ ] Analytics events fire only once per action.
## 9. Privacy / Security
- [ ] Sensitive inputs (password, token) are masked.
- [ ] Pasted passwords do not leak to clipboard monitors.
- [ ] Error states never echo back credentials.
## 10. Regression Hot Spots
- [ ] Recent bug areas retested (link to `bug-report-samples.md`).
- [ ] Feature-flag on/off combinations covered.
