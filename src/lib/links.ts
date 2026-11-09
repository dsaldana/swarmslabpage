/** YouTube links leave the lab site open in the visitor's current tab. */
export function isYouTubeUrl(value?: string): boolean {
  if (!value) return false;
  try {
    const url = new URL(value);
    return ['http:', 'https:'].includes(url.protocol) && (
      url.hostname === 'youtu.be' || url.hostname.endsWith('.youtu.be') ||
      url.hostname === 'youtube.com' || url.hostname.endsWith('.youtube.com')
    );
  } catch {
    return false;
  }
}

export function youtubeLinkAttributes(url?: string) {
  return isYouTubeUrl(url) ? { target: '_blank', rel: 'noopener noreferrer' } : {};
}
