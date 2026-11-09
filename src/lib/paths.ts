/** Prefix internal URLs for GitHub project Pages; also supports an apex domain. */
export function withBase(path: string): string {
  if (!path.startsWith('/') || path.startsWith('//')) return path;
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  if (base && (path === base || path.startsWith(base + '/'))) return path;
  const split = path.search(/[?#]/);
  const pathname = split < 0 ? path : path.slice(0, split);
  const suffix = split < 0 ? '' : path.slice(split);
  const normalized = /\.[a-z0-9]+$/i.test(pathname) || pathname.endsWith('/') ? pathname : pathname + '/';
  return base + normalized + suffix;
}
